from Piece import Piece

class Pawn(Piece):

    def __init__(self, color, row, col, moved):
        super().__init__(color, row, col)
        self.moved = moved

    def __repr__(self):
        return f"Pawn({self.color}, {self.row}, {self.col}, {self.moved})"
    
    def __eq__(self, other):
        if isinstance(other, Pawn):
            # Compare the attributes or properties that determine equality
            return self.color == other.color and self.row == other.row and self.col == other.col and self.moved == other.moved
        return False
    
    def seen_squares(self):
        row = self.row
        col = self.col
        moves = []

        #white moves up the board(negative) and black moves down the board(positive)
        direction = -1 if self.color == 1 else 1 

        #If hasnt moved, gets to go one more
        if not self.moved:
            new_row = row + 2 * direction
            if 0 <= new_row <= 7:
                moves.append((new_row, col))

        #Can always go one foward
        new_row = row + direction
        if 0 <= new_row <= 7:
            moves.append((new_row, col))

        #Capturing Diagonally
        for c in [-1, 1]:
            new_row = row + direction
            new_col = col + c
            if 0 <= new_col <= 7:
                moves.append((new_row, new_col))

        return moves

    def can_move_to(self, row, col):
        return (row, col) in self.seen_squares()