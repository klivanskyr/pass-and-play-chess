from Piece import Piece

class King(Piece):

    def __init__(self, color, row, col, moved, checked):
        super().__init__(color, row, col)
        self.moved = moved
        self.checked = checked
    
    def __repr__(self):
        return f"King({self.color}, {self.row}, {self.col}, {self.moved}, {self.checked})"
    
    def __eq__(self, other):
        if isinstance(other, King):
            # Compare the attributes or properties that determine equality
            return self.color == other.color and self.row == other.row and self.col == other.col and self.moved == other.moved and self.checked == other.checked
        return False
        
    def seen_squares(self):
        row = self.row
        col = self.col
        moves = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                new_row, new_col = row + i, col + j
                if 0 <= new_row < 8 and 0 <= new_col < 8 and (i != 0 or j != 0):
                    moves.append((new_row, new_col))

        return moves
    
    def can_move_to(self, row, col):
        return (row, col) in self.seen_squares()