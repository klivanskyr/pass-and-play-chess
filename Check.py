from King import King
from Queen import Queen
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Pawn import Pawn
from Open import Open
from Normal import Normal
from State import State
import copy

class Check(State):

    def __init__(self, turn, row, col, pieces, checkmate=False):
        super().__init__(turn, row, col, pieces)
        self.checkmate = checkmate
    
    def capture_at(self, released_row, released_col):
        clicked = self.pieces[self.row][self.col]
        released = self.pieces[released_row][released_col]
        print(clicked, released)

        #Cannot move empty square
        if (not isinstance(clicked, Open)) and (clicked.can_move_to(released.row, released.col)):
            #if pawn wants to go diagonally, needs to be an enemy piece there
            #cannot be same color
            #cannot be same square
            #cannot move an Open
            #cannot move a piece on the wrong turn
            #DOES NOT LOOK TO SEE IF MOVE RESULTS IN A CHECK FOR EITHER SIDE. THAT IS THE JOB OF UPDATE IN STATE
            
            #pawn moving columns cannot go to empty space.
            if released.col != self.col and isinstance(clicked, Pawn) and isinstance(released, Open):
                return self #Do not change anything / do not allow move
            
            #Pawn going foward can only go on empty spaces
            if released.col == self.col and isinstance(clicked, Pawn) and not isinstance(released, Open):
                return self #Do not change anything / do not allow move
            
            #cannot caputre same color
            if clicked.color == released.color:
                return self #Do not change anything / do not allow move
            
            #cannot move piece on wrong turn color
            if clicked.color != self.turn.color:
                return self #Do not change anything / do not allow move
            
            #Cannot take a piece if a sliding piece (bishop, rook, queen) is blocked by another piece
            if isinstance(clicked, Bishop) or isinstance(clicked, Rook) or isinstance(clicked, Queen):
                #if on the same column(vertical)
                if clicked.col == released.col:
                    print(1)
                    step = -1 if clicked.row > released.row else 1
                    for i in range(clicked.row + step, released.row, step):
                        if not isinstance(self.pieces[i][clicked.col], Open) and self.pieces[i][clicked.col] is not released:
                            return self
                    
                #if on the same row(horizontal)
                elif clicked.row == released.row:
                    print(2)
                    step = 1 if clicked.col < released.col else -1
                    for j in range(clicked.col + step, released.col, step):
                        if not isinstance(self.pieces[clicked.row][j], Open) and self.pieces[clicked.row][j] is not released:
                            return self

                #must be on diagonal if not on the rest
                elif abs(clicked.row - released.row) == abs(clicked.col - released.col):
                    print(3)
                    row_step = -1 if clicked.row > released.row else 1
                    col_step = 1 if clicked.col < released.col else -1
                    row, col = clicked.row + row_step, clicked.col + col_step
                    while (row, col) != (released.row, released.col):
                        if not isinstance(self.pieces[row][col], Open) and self.pieces[row][col] is not released:
                            print(3, self.pieces[row][col], released)
                            return self
                        row += row_step
                        col += col_step
            
            #If Pawn/King/Rook set moved to true
            if isinstance(clicked, King) or isinstance(clicked, Pawn) or isinstance(clicked, Rook):
                clicked.moved = True

            clicked.row = released.row
            clicked.col = released.col
            self.pieces[released.row][released.col] = clicked #change piece to new location
            self.pieces[self.row][self.col] = Open(self.row, self.col) #set old location to Open

            #Advance turn
            self.turn.advance_turn()

            print("SUCCESSFUL CAPTURE")

    def is_checkmate(self):
        #Looks at a position and determines if it is checkmate.
        #Check if king cannot move
        #Check if cannot be blocked
        #Check if cannot capture
        #If all are true, then it is checkmate

        old_color = 1 if self.turn.color == 0 else 0

        #Find attacking king, find checked king, list of all att pieces, list of all checked pieces
        all_att_pieces = []
        all_checked_pieces = []
        for i in range(len(self.pieces)):
            for j in range(len(self.pieces[i])):
                if isinstance(self.pieces[i][j], King) and self.pieces[i][j].color == old_color:
                    att_king = self.pieces[i][j]
                if isinstance(self.pieces[i][j], King) and self.pieces[i][j].color == self.turn.color:
                    checked_king = self.pieces[i][j]
                if self.pieces[i][j].color == old_color:
                    all_att_pieces.append(self.pieces[i][j])
                if self.pieces[i][j].color == self.turn.color:
                    all_checked_pieces.append(self.pieces[i][j])

        possible_squares = checked_king.seen_squares()
        cannot_move = True
        for i, j in possible_squares:
            temp = copy.deepcopy(self)
            temp.capture_at(i, j)
            temp.update()
            #if temp pieces change, the king was able to move to a safe location.
            if temp.pieces != self.pieces:
                cannot_move = False

        print(f"cannot move: {cannot_move}")

        #find attacking pieces that are attacking the king
        #Do this by having every attacking piece try to take the checked king. If they can, then they are currently attacking it
        checking_pieces = []
        for piece in all_att_pieces:
            temp = copy.deepcopy(self)
            #Set to having clicked on the piece
            temp.row = piece.row
            temp.col = piece.col
            #Set to having released on the checked king
            temp.capture_at(checked_king.row, checked_king.col)
            temp.update()
            #If temp pieces change, then that piece was attacking the king
            if temp.pieces != self.pieces:
                checking_pieces.append(piece)

        #May not be the right turn color to work correctly
        print(f"checking pieces: {checking_pieces}")

        #If there are no checking_pieces, then it can be blocked / cannot caputure attacker
        if len(checking_pieces) == 0:
            cannot_be_blocked = False
        #If there is more than one checking piece, then it cannot be blocked
        elif len(checking_pieces) > 1:
            cannot_be_blocked = True
        #If there is only one piece checking, see if that one piece can be blocked.
        elif len(checking_pieces) == 1:
            piece = checking_pieces[0]
            #Knight and Pawn cannot be blocked
            if isinstance(piece, Knight) or isinstance(piece, Pawn):
                cannot_be_blocked = True
            #Check sliding pieces
            else:
                attacked_squares = piece.seen_squares()

                #Try to move every checked piece on every attacked square. If any of them stop it from being check, then it can be blocked.
                found = False
                cannot_be_blocked = True
                for checked_piece in all_checked_pieces:
                    for r, c in attacked_squares:
                        temp = copy.deepcopy(self)
                        #Set clicked piece
                        temp.row = checked_piece.row
                        temp.col = checked_piece.col
                        #Set released square
                        temp.capture_at(r, c)
                        temp.update()
                        new_checked_king = temp.pieces.get(checked_king.row).get(checked_king.col)
                        #if the king has moved, then it cannot be blocked 
                        if new_checked_king.checked:
                            continue
                        else:
                            cannot_be_blocked = False
                            found = True
                            break
                    if found:
                        break
        
        print(f"Cannot be blocked: {cannot_be_blocked}")


        #Can capture attacker if no checking pieces
        if len(checking_pieces) == 0:
            cannot_capture_attacker = False
        elif len(checking_pieces) > 1:
            cannot_capture_attacker = True
        elif len(checking_pieces) == 1:
            piece = checking_pieces[0]
            cannot_capture_attacker = True
            for checked_piece in all_checked_pieces:
                temp = copy.deepcopy(self)
                #Set clicked piece
                temp.row = checked_piece.row
                temp.col = checked_piece.col
                #Set released square
                temp.capture_at(piece.row, piece.col)
                temp.update()

                for row in temp.pieces:
                    for elt in row:
                        if isinstance(elt, King) and elt.color == self.turn.color:
                            temp_king = elt
                
                if temp_king.checked:
                    continue
                else:
                    cannot_capture_attacker = False
                    break
            
        print(f"cannot capture attacker: {cannot_capture_attacker}")

        return isinstance(self, Check) and checked_king.checked and cannot_be_blocked and cannot_capture_attacker and cannot_move

                            


    #Check to see if the new position is valid
    def update(self, current):
        print(f"future color is: {self.turn.color}\ncurrent color is: {current.turn.color}")
        future = self
        #cannot have a king move into check (if the move results in a check)
        #cannot move a piece if it is pinned (if the move results in a check)

        #Check to see if something changed. If they just clicked the board or made an invalide move. Nothing should change
        if future.pieces == current.pieces:
            print("nothing changed")
            #print(future, current)
            return current
        
        #find the cur king in future pieces. If the current side made a move that put themselves in check,
        #They were pinned and should not have been able to make that move.
        for i in range(len(future.pieces)):
            for j in range(len(future.pieces[i])):
                if isinstance(future.pieces[i][j], King) and future.pieces[i][j].color == current.turn.color:
                    cur_king = future.pieces[i][j]

        #Get all the future sides pieces because we need to check if they can successfully take the king
        #If they can, they we know that the king should be in check, and thus the current side should not 
        #have been able to make the move.
        cur_king_is_in_check = False
        for i in range(len(future.pieces)):
            for j in range(len(future.pieces[i])):
                if future.pieces[i][j].color == future.turn.color:
                    temp = copy.deepcopy(future)
                    temp.row = i
                    temp.col = j
                    temp.capture_at(cur_king.row, cur_king.col)
                    #if temp is able to capture the king, the pieces will change, so we can detect this
                    if temp.pieces != future.pieces:
                        cur_king_is_in_check = True
        
        #Find the future king in the future pieces.
        for i in range(len(future.pieces)):
            for j in range(len(future.pieces[i])):
                if isinstance(future.pieces[i][j], King) and future.pieces[i][j].color == future.turn.color:
                    future_king = future.pieces[i][j]

        #If the future king is can be taken by the cur pieces. It is now in check
        future_king_is_in_check = False
        for i in range(len(future.pieces)):
            for j in range(len(future.pieces[i])):
                if future.pieces[i][j].color == current.turn.color:
                    temp = copy.deepcopy(future)
                    temp.row = i
                    temp.col = j
                    temp.turn.color = current.turn.color
                    temp.capture_at(future_king.row, future_king.col)
                    #if temp is able to capture the king, the pieces will change, so we can detect this
                    if temp.pieces != future.pieces:
                        future_king_is_in_check = True


        #If the cur king and future king arent in check, it was just a normal move and can be played
        if not cur_king_is_in_check and not future_king_is_in_check:
            print(11, future.turn.color)
            return future
        #If the current is not in check, and the future is in check. Set the future king to checked and update state
        if not cur_king_is_in_check and future_king_is_in_check:
            print(22)
            future_king.checked = True
            return Check(future.turn, future.row, future.col, future.pieces)
        #If the cur king was checked but now it is not, return state to normal and removed checked
        if not cur_king_is_in_check and cur_king.checked:
            print(33)
            future_king.checked = False
            return Normal(future.turn, future.row, future.col, future.pieces)
        #If the cur king is in check, whatever piece was moved was pinned and so the move should have never happened
        if cur_king_is_in_check:
            print(44)
            return current