class Piece:
    def __init__(self, color, row, col, last_piece_moved=False):
        if color not in [None, 0, 1]:
            raise ValueError(f"Color must be 0 for black, 1 for white or None for open space")
        self.color = color
        self.row = row
        self.col = col
    
