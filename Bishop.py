from Piece import Piece

class Bishop(Piece):

    def __init__(self, color, row, col):
        super().__init__(color, row, col)

    def __repr__(self):
        return f"Bishop({self.color}, {self.row}, {self.col})"
    
    def __eq__(self, other):
        if isinstance(other, Bishop):
            # Compare the attributes or properties that determine equality
            return self.color == other.color and self.row == other.row and self.col == other.col
        return False
    
    def seen_squares(self):
        row = self.row
        col = self.col
        moves = []

        #up-right
        for i in range(1, min(8 - row, 8 - col)):
            moves.append((row + i, col + i))

        #up-left
        for i in range(1, min(8 - row, col + 1)):
            moves.append((row + i, col - i))

        #down-right
        for i in range(1, min(row + 1, 8 - col)):
            moves.append((row - i, col + i))

        #down-left
        for i in range(1, min(row + 1, col + 1)):
            moves.append((row - i, col - i))

        return moves
    
    def can_move_to(self, row, col):
        return (row, col) in self.seen_squares()
