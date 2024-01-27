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