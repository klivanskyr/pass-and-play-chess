from State import State


class Normal(State):

    def __init__(self, turn, row, col, pieces):
        super().__init__(turn, row, col, pieces)