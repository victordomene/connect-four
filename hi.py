from copy import copy, deepcopy
import random

INFINITY = 100
random.seed()

COLSNUM = 7
ROWSNUM = 6

def negamax(board, depth, color):
    #print "STARTING MINIMAX"
    score = board.get_score()

    if depth == 0:
        return (color * score, None)
    else:
        maxValue = -INFINITY
        maxMove = None

        for i in range(0,7):
            c = deepcopy(board)
            if (not board.cannot_play_in(i)):
                oldValue = maxValue
                oldMove = maxMove

                try:
                    c.play(i)
                    (scr, move) = negamax(c, depth - 1, -1*color)
                    scr = -scr

                    #print "scr: {}   -   maxValue: {}".format(scr, maxValue)

                    if scr >= maxValue:
                        maxValue = scr
                        maxMove = i

                    #print "{}{}".format("maxValue: ", maxValue)
                    #print "{}{}".format("maxMove: ", maxMove)

                except ValueError, e:
                    if e.message == "ColumnFull":
                        maxValue = oldValue
                        maxMove = oldMove
                    else:
                        raise ValueError, e

        return (maxValue, maxMove)


class Board(object):
    """docstring for Board"""
    def __init__(self):
        super(Board, self).__init__()
        self.reset()

    def reset(self):
        b = ['.','.','.','.','.','.']
        self.cols = [copy(b),copy(b),copy(b),copy(b),copy(b),copy(b),copy(b)]
        self.current_player = "X"

    def cannot_play_in(self, col):
        return not ('.' in self.cols[col])


    def get_player(self):
        return self.current_player

    def switch_player(self):
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

    def lowest_available(self, col):
        for i, sq in enumerate(self.cols[col]):
            if sq == '.':
                return i

    # 1-indexed cols
    def play(self, col):
        assert 0 <= col < 7
        if (not self.cannot_play_in(col)):
            self.cols[col][self.lowest_available(col)] = self.current_player
            self.switch_player()
        else:
            raise ValueError("ColumnFull")

    def transpose(self, l):
        # http://stackoverflow.com/a/11387441/2228485
        return [list(i) for i in zip(*l)]

    def display_board(self):
        # mutability makes this more difficult than it probably should be
        # Copy self.cols. Reverse every column
        col_copy = deepcopy(self.cols)
        for c in col_copy:
            c.reverse()
        for r in self.transpose(col_copy):
            print "{} {} {} {} {} {} {}".format(*r)

    def copy_board(self):
        return deepcopy(self.cols)

    def play_random(self):
        x = random.randint(0,7)
        while (self.cannot_play_in(x)):
            x = random.randint(0,7)
        self.play(x)

    def get_score(self):
        score = 0

        for i in range(0, COLSNUM - 3):
            for j in range(0, ROWSNUM - 3):
                fours = [[],[]]

                for x in range (0,10):
                    fours[0].append(0)
                    fours[1].append(0)

                for k in range(0,4):
                    for m in range(0,4):
                        if (self.cols[i+k][j+m] != "."):
                            if (self.cols[i+k][j+m] == "X"):
                                index = 0
                            elif (self.cols[i+k][j+m] == "O"):
                                index = 1

                            fours[index][k] += 1
                            fours[index][m+4] += 1
                            if (k == m):
                                fours[index][8] += 1
                            elif (k == 3-m):
                                fours[index][9] += 1

                for k in range(0,10):
                    if (fours[0][k] == 4):
                        return -1
                    elif (fours[1][k] == 4):
                        return 1
        return score

    def winning(self):
        flag = False

        for i in range(0, COLSNUM - 3):
            for j in range(0, ROWSNUM - 3):
                fours = [[],[]]

                for x in range (0,10):
                    fours[0].append(0)
                    fours[1].append(0)

                for k in range(0,4):
                    for m in range(0,4):
                        if (self.cols[i+k][j+m] != "."):
                            if (self.cols[i+k][j+m] == "X"):
                                index = 0
                            elif (self.cols[i+k][j+m] == "O"):
                                index = 1

                            fours[index][k] += 1
                            fours[index][m+4] += 1
                            if (k == m):
                                fours[index][8] += 1
                            elif (k == 3-m):
                                fours[index][9] += 1

                for k in range(0,10):
                    if (fours[0][k] == 4) or (fours[1][k] == 4):
                        flag = True
        return flag

def multiplayer():
    b = Board()
    b.display_board
    while(True):
        play = input("Where to play?: ")
        b.play(play-1)
        b.display_board()

def singleplayer():
    b = Board()
    b.display_board

    while(not b.winning()):
        while(b.get_player() == "X"):
            flag = 0
            while (flag == 0):
                try:
                    play = input("Where to play?: ")
                    flag = 1
                except NameError as e:
                    print "Type in an INTEGER!"
                    flag = 0

            try:
                b.play(play-1)
            except ValueError as e:
                if e.message == "ColumnFull":
                    print "This column is already full. Please pick a different one."
                else:
                    raise ValueError(e)
            except AssertionError:
                print "Type in a valid integer!"

        (score, move) = negamax(b, 6, 1)
        if (move is not None):
            try:
                b.play(move)
            except ValueError as e:
                if e.message == "ColumnFull":
                    pass
                else:
                    raise ValueError(e)
        else:
            b.play_random()

        b.display_board()

def main():
    singleplayer()

if __name__ == "__main__":
    main ()