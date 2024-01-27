from Piece import Piece

class Knight(Piece):

    def __init__(self, color, row, col):
        super().__init__(color, row, col)

    def __repr__(self):
        return f"Knight({self.color}, {self.row}, {self.col})"
    
    def __eq__(self, other):
        if isinstance(other, Knight):
            # Compare the attributes or properties that determine equality
            return self.color == other.color and self.row == other.row and self.col == other.col
        return False
    
    def seen_squares(self):
        row = self.row
        col = self.col
        moves = []

        knight_moves_offsets = [
        (2, 1), (1, 2), (-1, 2), (-2, 1),
        (-2, -1), (-1, -2), (1, -2), (2, -1)
        ]

        for offset_row, offset_col in knight_moves_offsets:
            new_row, new_col = row + offset_row, col + offset_col
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                moves.append((new_row, new_col))

        return moves
    
    def can_move_to(self, row, col):
        return (row, col) in self.seen_squares()