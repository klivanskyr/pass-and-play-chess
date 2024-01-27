from Piece import Piece

class Open(Piece):

    def __init__(self, row, col, color=None):
        super().__init__(color, row, col)

    def __repr__(self):
        return f"Open({self.row}, {self.col})"
    
    def __eq__(self, other):
        if isinstance(other, Open):
            # Compare the attributes or properties that determine equality
            return self.row == other.row and self.col == other.col
        return False