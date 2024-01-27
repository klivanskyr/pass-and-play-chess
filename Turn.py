class Turn:

    def __init__(self, color, number):
        self.color = color
        self.number = number

    def advance_turn(self):
        if self.color == 1: #If its whites turn, make it blacks turn
            self.color = 0
        else: #If its blacks, make it whites turn and increase the counter by 1
            self.color = 1
            self.number += 1
