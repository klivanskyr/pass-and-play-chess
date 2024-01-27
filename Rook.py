from Piece import Piece

class Rook(Piece):

    def __init__(self, color, row, col, moved):
        super().__init__(color, row, col)
        self.moved = moved
    
    def __repr__(self):
        return f"Rook({self.color}, {self.row}, {self.col}, {self.moved})"
    
    def __eq__(self, other):
        if isinstance(other, Rook):
            # Compare the attributes or properties that determine equality
            return self.color == other.color and self.row == other.row and self.col == other.col and self.moved == other.moved
        return False
    
    def seen_squares(self):
        row = self.row
        col = self.col
        moves = []

        #horizontal
        for new_col in range(8):
            if new_col != col:
                moves.append((row, new_col))

        #vertical
        for new_row in range(8):
            if new_row != row:
                moves.append((new_row, col))

        return moves
    
    def can_move_to(self, row, col):
        return (row, col) in self.seen_squares()