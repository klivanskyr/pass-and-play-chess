import pygame
import copy
from State import State
from Imagehandler import Imagehandler
from Normal import Normal
from Check import Check
from Turn import Turn
from Fenconverter import Fenconverter
from King import King
from Queen import Queen
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Pawn import Pawn
from Open import Open


def main():
    pygame.init()

    #CONSTANTS FOR WIDTH AND HEIGHT
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    PIECE_WIDTH = 97
    PIECE_HEIGHT = 97
    BOARD_SIZE = 8
    SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE

    #COLORS
    BEIGE = (240, 230, 209)
    GREEN = (62, 130, 61)
    YELLOW = (150, 150, 0)


    #CREATE SCREEN AND ITS CAPTION
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("its chess bruv!")

    #IMAGE IMPORTS
    #chess_board_png = Imagehandler("https://i.stack.imgur.com/s8XND.png", SCREEN_WIDTH, SCREEN_HEIGHT).image
    b_king_png = Imagehandler("https://www.symbols.com/images/symbol/3398_black-king.png", PIECE_WIDTH, PIECE_HEIGHT).image
    w_king_png = Imagehandler("https://www.symbols.com/images/symbol/1/3404_white-king.png", PIECE_WIDTH, PIECE_HEIGHT).image
    b_queen_png = Imagehandler("https://www.symbols.com/images/symbol/3399_black-queen.png", PIECE_WIDTH, PIECE_HEIGHT).image
    w_queen_png = Imagehandler("https://www.symbols.com/images/symbol/1/3405_white-queen.png", PIECE_WIDTH, PIECE_HEIGHT).image
    b_bishop_png = Imagehandler("https://www.symbols.com/images/symbol/1/3401_black-bishop.png", PIECE_WIDTH, PIECE_HEIGHT).image
    w_bishop_png = Imagehandler("https://www.symbols.com/images/symbol/1/3407_white-bishop.png", PIECE_WIDTH, PIECE_HEIGHT).image
    b_knight_png = Imagehandler("https://www.symbols.com/images/symbol/1/3402_black-knight.png", PIECE_WIDTH, PIECE_HEIGHT).image
    w_knight_png = Imagehandler("https://www.symbols.com/images/symbol/1/3408_white-knight.png", PIECE_WIDTH, PIECE_HEIGHT).image
    b_pawn_png = Imagehandler("https://www.symbols.com/images/symbol/1/3403_black-pawn.png", PIECE_WIDTH, PIECE_HEIGHT).image
    w_pawn_png = Imagehandler("https://www.symbols.com/images/symbol/1/3409_white-pawn.png", PIECE_WIDTH, PIECE_HEIGHT).image
    b_rook_png = Imagehandler("https://www.symbols.com/images/symbol/1/3400_black-rook.png", PIECE_WIDTH, PIECE_HEIGHT).image
    w_rook_png = Imagehandler("https://www.symbols.com/images/symbol/1/3406_white-rook.png", PIECE_WIDTH, PIECE_HEIGHT).image

    #Creation of the init state
    STARTING_FEN_CODE = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    starting_pis = Fenconverter(STARTING_FEN_CODE).convert()
    state = Normal(Turn(1, 1), None, None, starting_pis)

    #Function for placing a matrix of Piece Objects into the scene
    def draw(state):
        if state.last_piece_from != None:
            #Flip row
            last_from_row, last_from_col = state.last_piece_from
            last_to_row, last_to_col = state.last_piece_to
            if state.turn.color == 0:
                last_from_row = 7 - last_from_row
                last_to_row = 7 - last_to_row   

            #Drawing last move alpha
            from_temp_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            from_temp_surface.set_alpha(100)
            from_temp_surface.fill(YELLOW)
            screen.blit(from_temp_surface, (last_from_col * SQUARE_SIZE, last_from_row * SQUARE_SIZE))

            to_temp_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            to_temp_surface.set_alpha(100)
            to_temp_surface.fill(YELLOW)
            screen.blit(to_temp_surface, (last_to_col * SQUARE_SIZE, last_to_row * SQUARE_SIZE))

        #Drawing pieces
        pieces = state.pieces
        for r in range(len(pieces)):
            for c in range(len(pieces[r])):
                piece = pieces[r][c]
                if state.turn.color == 1:
                    if isinstance(piece, Pawn):
                        if piece.color == 1:
                            screen.blit(w_pawn_png, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                        else:
                            screen.blit(b_pawn_png, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                    elif isinstance(piece, Rook):
                        if piece.color == 1:
                            screen.blit(w_rook_png, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                        else:
                            screen.blit(b_rook_png, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                    elif isinstance(piece, Knight):
                        if piece.color == 1:
                            screen.blit(w_knight_png, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                        else:
                            screen.blit(b_knight_png, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                    elif isinstance(piece, Bishop):
                        if piece.color == 1:
                            screen.blit(w_bishop_png, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                        else:
                            screen.blit(b_bishop_png, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                    elif isinstance(piece, Queen):
                        if piece.color == 1:
                            screen.blit(w_queen_png, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                        else:
                            screen.blit(b_queen_png, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                    elif isinstance(piece, King):
                        if piece.checked:
                            temp_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                            temp_surface.set_alpha(128)
                            temp_surface.fill((255, 0, 0))
                            screen.blit(temp_surface, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                        if piece.color == 1:
                            screen.blit(w_king_png, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                        elif piece.color == 0:
                            screen.blit(b_king_png, (c * SQUARE_SIZE, r * SQUARE_SIZE))
                    elif isinstance(piece, Open):
                        continue
                else:
                    if isinstance(piece, Pawn):
                        if piece.color == 1:
                            screen.blit(w_pawn_png, (c * SQUARE_SIZE, (7 - r) * SQUARE_SIZE))
                        else:
                            screen.blit(b_pawn_png, (c * SQUARE_SIZE, (7 - r) * SQUARE_SIZE))
                    elif isinstance(piece, Rook):
                        if piece.color == 1:
                            screen.blit(w_rook_png, (c * SQUARE_SIZE, (7 - r) * SQUARE_SIZE))
                        else:
                            screen.blit(b_rook_png, (c * SQUARE_SIZE, (7 - r) * SQUARE_SIZE))
                    elif isinstance(piece, Knight):
                        if piece.color == 1:
                            screen.blit(w_knight_png, (c * SQUARE_SIZE, (7 - r) * SQUARE_SIZE))
                        else:
                            screen.blit(b_knight_png, (c * SQUARE_SIZE, (7 - r) * SQUARE_SIZE))
                    elif isinstance(piece, Bishop):
                        if piece.color == 1:
                            screen.blit(w_bishop_png, (c * SQUARE_SIZE, (7 - r) * SQUARE_SIZE))
                        else:
                            screen.blit(b_bishop_png, (c * SQUARE_SIZE, (7 - r) * SQUARE_SIZE))
                    elif isinstance(piece, Queen):
                        if piece.color == 1:
                            screen.blit(w_queen_png, (c * SQUARE_SIZE, (7 - r) * SQUARE_SIZE))
                        else:
                            screen.blit(b_queen_png, (c * SQUARE_SIZE, (7 - r) * SQUARE_SIZE))
                    elif isinstance(piece, King):
                        if piece.checked:
                            temp_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                            temp_surface.set_alpha(128)
                            temp_surface.fill((255, 0, 0))
                            screen.blit(temp_surface, (c * SQUARE_SIZE, (7 - r) * SQUARE_SIZE))
                        if piece.color == 1:
                            screen.blit(w_king_png, (c * SQUARE_SIZE, (7 - r) * SQUARE_SIZE))
                        elif piece.color == 0:
                            screen.blit(b_king_png, (c * SQUARE_SIZE, (7 - r) * SQUARE_SIZE))
                    elif isinstance(piece, Open):
                        continue

    #For checkmate / end game screen
    def draw_checkmate(state):
        draw(state)
        # Set up font
        font = pygame.font.Font(None, 96)  # You can specify the font file and size here

        # Set up text
        winner = "White" if state.turn.color == 0 else "Black"

        text = "Checkmate. " + winner + " wins!"
        text_surface = font.render(text, True, (0, 0, 0))  # Text color is black

        # Set up text position
        text_rect = text_surface.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        screen.blit(text_surface, text_rect)


    #MAIN LOOP
    print("\nStarted")
    checkmate = False
    run = True
    while run:
        #Draw Background Board
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = BEIGE if (row + col) % 2 == 0 else GREEN
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        #Piece Drawer
        if isinstance(state, Check) and state.checkmate == True:
            checkmate = True
            run = False
        else:
            draw(state)
            #Event Handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Exited\n")
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x = event.pos[0]
                    y = event.pos[1]

                    row = int(y // SQUARE_SIZE)
                    col = int(x // SQUARE_SIZE)

                    if state.turn.color == 0:
                        row = 7 - row

                    state.row = row
                    state.col = col
                    print(f"Pressed at {row}, {col}\n")
                elif event.type == pygame.MOUSEBUTTONUP:
                    x = event.pos[0]
                    y = event.pos[1]
                        
                    row = int(y // SQUARE_SIZE)
                    col = int(x // SQUARE_SIZE)

                    if state.turn.color == 0:
                        row = 7 - row

                    before_capture = copy.deepcopy(state)
                    state.capture_at(row, col)                
                    state = update(state, before_capture)
                    if before_capture.turn.color != state.turn.color:
                        state.last_piece_from = (state.row, state.col)
                        state.last_piece_to = (row, col)
                    if isinstance(state, Check) and is_checkmate(state):
                        state.checkmate = True

                    print(f"Released at {row}, {col}")
                    print("NEXT TURN\n\n\n")

        pygame.display.update()

    pygame.display.update()

    print(f"checkmate: {checkmate}")
    while checkmate:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        draw_checkmate(state)
        

        pygame.display.update()






#Logic for checking if a poisiton is a valid updated position
#Check to see if the new position is valid
def update(future, current) -> State:
    #cannot have a king move into check (if the move results in a check)
    #cannot move a piece if it is pinned (if the move results in a check)

    #Check to see if something changed. If they just clicked the board or made an invalide move. Nothing should change
    if future.pieces == current.pieces:
        #print("nothing changed")
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

    #If the future king can be taken by the cur pieces. It is now in check
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


    #print(cur_king_is_in_check, cur_king.checked, future_king_is_in_check)
    #If the cur king and future king arent in check, it was just a normal move and can be played
    if not cur_king_is_in_check and not future_king_is_in_check and not cur_king.checked:
        #print(11)
        return future
    #If the current is not in check, and the future is in check. Set the future king to checked and update state
    if not cur_king_is_in_check and future_king_is_in_check:
        #print(22)
        future_king.checked = True
        return Check(future.turn, future.row, future.col, future.pieces)
    #If the cur king was checked but now it is not, return state to normal and removed checked
    if not cur_king_is_in_check and cur_king.checked:
        #print(33)
        cur_king.checked = False
        return Normal(future.turn, future.row, future.col, future.pieces)
    #If the cur king is in check, whatever piece was moved was pinned and so the move should have never happened
    if cur_king_is_in_check:
        #print(44)
        return current

    
#Logic for checking if a position is checkmate
def is_checkmate(state) -> bool:
        #Looks at a position and determines if it is checkmate.
        #Check if king cannot move
        #Check if cannot be blocked
        #Check if cannot capture
        #If all are true, then it is checkmate

        old_color = 1 if state.turn.color == 0 else 0

        #Find attacking king, find checked king, list of all att pieces, list of all checked pieces
        all_att_pieces = []
        all_checked_pieces = []
        for i in range(len(state.pieces)):
            for j in range(len(state.pieces[i])):
                if isinstance(state.pieces[i][j], King) and state.pieces[i][j].color == old_color:
                    att_king = state.pieces[i][j]
                if isinstance(state.pieces[i][j], King) and state.pieces[i][j].color == state.turn.color:
                    checked_king = state.pieces[i][j]
                if state.pieces[i][j].color == old_color:
                    all_att_pieces.append(state.pieces[i][j])
                if state.pieces[i][j].color == state.turn.color:
                    all_checked_pieces.append(state.pieces[i][j])

        possible_squares = checked_king.seen_squares()
        cannot_move = True
        for i, j in possible_squares:
            temp = copy.deepcopy(state)
            #Set to having clicked on the piece
            temp.row = checked_king.row
            temp.col = checked_king.col
            #Try to capture anywhere
            temp.capture_at(i, j)
            temp = update(temp, state)
            #if temp pieces change, the king was able to move to a safe location.
            if temp.pieces != state.pieces:
                cannot_move = False

        print(f"cannot move: {cannot_move}")

        #find attacking pieces that are attacking the king
        #Do this by having every attacking piece try to take the checked king. If they can, then they are currently attacking it
        checking_pieces = []
        for piece in all_att_pieces:
            temp = copy.deepcopy(state)
            #Set it to old color turn so capture at works
            temp.turn.color = old_color
            #Set to having clicked on the piece
            temp.row = piece.row
            temp.col = piece.col
            #Try to capture checked king
            temp.capture_at(checked_king.row, checked_king.col)
            try:
                #If cannot find the king, then that piece can take it and is checking it
                update(temp, state)
            except:
                checking_pieces.append(piece)

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
                        temp = copy.deepcopy(state)
                        #Set clicked piece
                        temp.row = checked_piece.row
                        temp.col = checked_piece.col
                        #Set released square
                        temp.capture_at(r, c)
                        temp = update(temp, state)
                        new_checked_king = temp.pieces[checked_king.row][checked_king.col]
                        #if the king has moved, then it cannot be blocked 
                        if isinstance(new_checked_king, King) and not new_checked_king.checked:
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
                temp = copy.deepcopy(state)
                #Set clicked piece
                temp.row = checked_piece.row
                temp.col = checked_piece.col
                #Set released 
                temp.capture_at(piece.row, piece.col)
                temp = update(temp, state)

                if temp.pieces != state.pieces:
                    print(f"{checked_piece} CAN CAPTURE!")
                    cannot_capture_attacker = False
                    break
            
        print(f"cannot capture attacker: {cannot_capture_attacker}")

        return isinstance(state, Check) and checked_king.checked and cannot_be_blocked and cannot_capture_attacker and cannot_move

if __name__ == "__main__":
    main()


