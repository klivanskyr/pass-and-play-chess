from King import King
from Queen import Queen
from Rook import Rook
from Bishop import Bishop
from Pawn import Pawn
from Open import Open

class State:
    
    def __init__(self, turn, row, col, pieces, last_piece_from=None, last_piece_to=None):
        self.turn = turn
        self.row = row
        self.col = col
        self.pieces = pieces
        self.last_piece_from = last_piece_from
        self.last_piece_to = last_piece_to

    def __str__(self) -> str:
        if self.turn.color == 1: 
            color = "White" 
        else: 
            color = "Black"

        return f"It is turn number {self.turn.number}.\nIt is {color}'s turn.\nThe last clicked square is ({self.row}, {self.col}).\nThe position of all the pieces are:\n{self.pieces}."
    
    def capture_at(self, released_row, released_col):
        clicked = self.pieces[self.row][self.col]
        released = self.pieces[released_row][released_col]

        #Castling logic
        if isinstance(clicked, King) and not clicked.moved:
            if clicked.color == 1 and (clicked.row, clicked.col) == (7, 4):
                #White Short
                if ((released.row, released.col) == (7, 6) or (released.row, released.col) == (7, 7)) and isinstance(self.pieces[7][5], Open) and isinstance(self.pieces[7][6], Open) and isinstance(self.pieces[7][7], Rook) and not self.pieces[7][7].moved:
                    self.pieces[7][6] = clicked #king in corner
                    self.pieces[7][2].moved = True #Set King moved to True
                    self.pieces[7][4] = Open(7, 4) #replace king with open
                    self.pieces[7][5] = self.pieces[7][7] #put rook to the left of king
                    self.pieces[7][5].moved = True #Set rook moved to True
                    self.pieces[7][7] = Open(7, 7) #replace rook with open
                    self.turn.advance_turn()
                    return
                
                #White Long
                elif ((released.row, released.col) == (7, 1) or (released.row, released_col) == (7, 2)) and isinstance(self.pieces[7][3], Open) and isinstance(self.pieces[7][2], Open) and isinstance(self.pieces[7][1], Open) and isinstance(self.pieces[7][0], Rook) and not self.pieces[7][0].moved:
                    self.pieces[7][2] = clicked #king in corner
                    self.pieces[7][2].moved = True #Set King moved to True
                    self.pieces[7][4] = Open(7, 4) #replace king with open
                    self.pieces[7][3] = self.pieces[7][0] #put rook to the left of king
                    self.pieces[7][3].moved = True #Set rook moved to True
                    self.pieces[7][0] = Open(7, 0) #replace rook with open
                    self.turn.advance_turn()
                    return

            elif clicked.color == 0:
                #Black Short
                if ((released.row, released.col) == (0, 6) or (released.row, released.col) == (0, 7)) and isinstance(self.pieces[0][5], Open) and isinstance(self.pieces[0][6], Open) and isinstance(self.pieces[0][7], Rook) and not self.pieces[0][7].moved:
                    self.pieces[0][6] = clicked #king in corner
                    self.pieces[0][6].moved = True #Set King moved to True
                    self.pieces[0][4] = Open(0, 4) #replace king with open
                    self.pieces[0][5] = self.pieces[0][7] #put rook to the left of king
                    self.pieces[0][5].moved = True #Set rook moved to True
                    self.pieces[0][7] = Open(0, 7) #replace rook with open
                    self.turn.advance_turn()
                    return
                
                #Black Long
                elif ((released.row, released.col) == (0, 1) or (released.row, released_col) == (0, 2)) and isinstance(self.pieces[0][3], Open) and isinstance(self.pieces[0][2], Open) and isinstance(self.pieces[0][1], Open) and isinstance(self.pieces[0][0], Rook) and not self.pieces[0][0].moved:
                    self.pieces[0][2] = clicked #king in corner
                    self.pieces[0][2].moved = True #Set King moved to True
                    self.pieces[0][4] = Open(0, 4) #replace king with open
                    self.pieces[0][3] = self.pieces[0][0] #put rook to the left of king
                    self.pieces[0][3].moved = True #Set rook moved to True
                    self.pieces[0][0] = Open(0, 0) #replace rook with open
                    self.turn.advance_turn()
                    return
                    
        #Cannot move empty square
        if (not isinstance(clicked, Open)) and (clicked.can_move_to(released.row, released.col)):
            #if pawn wants to go diagonally, needs to be an enemy piece there
            #cannot be same color
            #cannot be same square
            #cannot move an Open
            #cannot move a piece on the wrong turn
            #DOES NOT LOOK TO SEE IF MOVE RESULTS IN A CHECK FOR EITHER SIDE. THAT IS THE JOB OF UPDATE
            
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
                    step = -1 if clicked.row > released.row else 1
                    for i in range(clicked.row + step, released.row, step):
                        if not isinstance(self.pieces[i][clicked.col], Open):
                            return self
                    
                #if on the same row(horizontal)
                elif clicked.row == released.row:
                    step = 1 if clicked.col < released.col else -1
                    for j in range(clicked.col + step, released.col, step):
                        if not isinstance(self.pieces[clicked.row][j], Open):
                            return self

                #must be on diagonal if not on the rest
                elif abs(clicked.row - released.row) == abs(clicked.col - released.col):
                    row_step = -1 if clicked.row > released.row else 1
                    col_step = 1 if clicked.col < released.col else -1
                    row, col = clicked.row + row_step, clicked.col + col_step
                    while (row, col) != (released.row, released.col):
                        if not isinstance(self.pieces[row][col], Open):
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