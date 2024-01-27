from King import King
from Queen import Queen
from Rook import Rook
from Knight import Knight
from Bishop import Bishop
from Pawn import Pawn
from Open import Open

class Fenconverter:

    def __init__(self, fen_code: str):
        self.fen_code = fen_code

    def convert(self):
        rows = self.fen_code.split("/")
        output = []
        for i in range(len(rows)):
            row_builder = []
            for j in range(len(rows[i])):
                match rows[i][j]:
                    case "r": row_builder.append(Rook(0, i, j, False))
                    case "R": row_builder.append(Rook(1, i, j, False))
                    case "n": row_builder.append(Knight(0, i, j))
                    case "N": row_builder.append(Knight(1, i, j))
                    case "b": row_builder.append(Bishop(0, i, j))
                    case "B": row_builder.append(Bishop(1, i, j))
                    case "k": row_builder.append(King(0, i, j, False, False))
                    case "K": row_builder.append(King(1, i, j, False, False))
                    case "q": row_builder.append(Queen(0, i, j))
                    case "Q": row_builder.append(Queen(1, i, j))
                    case "p": row_builder.append(Pawn(0, i, j, False))
                    case "P": row_builder.append(Pawn(1, i, j, False))
                    case _: 
                        for _ in range(int(rows[i][j])):
                            row_builder.append(Open(i, j))
                            j += 1
            
            output.append(row_builder)
        return output