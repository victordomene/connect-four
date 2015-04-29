from copy import copy, deepcopy
import random

INFINITY = 100
random.seed()

def negamax(board, plyr, depth, color):
	score = board.get_score()

	if depth == 0:
		return (color * score, None)
	else:
		maxValue = -INFINITY
		maxMove = None

		for i in range(0,6):
			c = deepcopy(board)
			if (not board.cannot_play_in(i)):
				oldValue = maxValue
				oldMove = maxMove
				try:
					c.play(i)
					(scr, move) = negamax(c, plyr, depth - 1, -1*color)
					scr = -scr
					if scr >= maxValue:
						maxValue = scr
						maxMove = i
					break
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

	def get_score(plyr):
		return random.randint(-1,1)

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

	while(True):
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
				break
			except ValueError as e:
				if e.message == "ColumnFull":
					print "This column is already full. Please pick a different one."
				else:
					raise ValueError(e)
			except AssertionError:
				print "Type in a valid integer!"

		(score, move) = negamax(b, "X", 0, 1)
		if (move is not None):
			try:
				b.play(move)
			except ValueError as e:
				if e.message == "ColumnFull":
					print "AI fucking up"
				else:
					raise ValueError(e)
		else:
			x = random.randint(0,6)
			while (b.cannot_play_in(x)):
				x = random.randint(0,6)
			b.play(x)

		b.display_board()

def main():
	singleplayer()

if __name__ == "__main__":
	main ()