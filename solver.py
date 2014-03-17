__author__ = "byronhulcher"

# This program will support any Row/Column size, they are not required to be equal
# To create a tic-tac-toe board, set board to be 3x3, and set CONSECUTIVATE_VALUE_WIN_CONDITION to be 3
# To create Connect Four, set board to be 7x6, and set CONSECUTIVATE_VALUE_WIN_CONDITION to be 4

# Game board, please use None for empty spaces!
board = [
	["x", None, "x"], 
	["o", "x", "o"], 
	["x", "o", "o"],
]

# The number of spaces which must contain the same value in a row to win
consecutive_value_win_condition = 3

# Tuples for the direction our scanners travel in
HORIZONTAL_DIRECTION_TUPLE = (0,1)
VERTICAL_DIRECTION_TUPLE = (1,0)
DESCENDING_DIAGONAL_DIRECTION_TUPLE = (1,1)
ASCENDING_DIAGONAL_DIRECTION_TUPLE = (-1,1)

# Custom Exceptions
class EmptyElementException(Exception):
	pass

class OutOfBoundsException(Exception):
	pass

# Singleton class that is responsible for managing scanners across a game board
class ScannerManager:
	def __init__(self, board):
		self.board = board
		self.scanners = {}

	# Generate a scanner at starting_x_y_tuple, travalling along direction direction_tuple, and save it
	def add_scanner(self, starting_x_y_tuple, direction_tuple):
		try:
			scanner = Scanner(starting_x_y_tuple, self.board[starting_x_y_tuple[0]][starting_x_y_tuple[1]], direction_tuple)
		except EmptyElementException:
			# Scanners cannot be initialized on an empty space
			return False
		else:
			key = "%s_%s_%s_%s" % (starting_x_y_tuple[0],  starting_x_y_tuple[1], direction_tuple[0], direction_tuple[1])
			self.scanners[key] = scanner
			return scanner

	# Iterate of all scanners, cleaning them up as they encounter errors
	def advance_all_scanners(self):
		for scanner_key in self.scanners.keys():
			scanner = self.scanners[scanner_key]
			try:
				new_value = self.advance_one_scanner(scanner)
			except (OutOfBoundsException, EmptyElementException):
				# Scanner has gone out of bounds of the board, or has stumbled on a blank space, so remove it
				del self.scanners[scanner_key]
				continue
			if new_value != scanner.value:
				# Scanner has encountered a different value, so remove it
				del self.scanners[scanner_key]
				continue

	def advance_one_scanner(self, scanner):
		scanner.advance()
		try:
			new_value = self.board[scanner.x][scanner.y]
		except IndexError:
			# The scanner has gone out of the array bounds
			raise OutOfBoundsException
		if not new_value:
			# The scanner has stumbled upon an empty space
			raise EmptyElementException
		# The scanner has successfully reached a new space with a matching value
		return new_value

class Scanner:
	def __init__(self, starting_x_y_tuple, starting_value, direction_tuple):
		if not starting_value:
			# Scanners cannot be initialized on an empty space
			raise EmptyElementException
		self.x = starting_x_y_tuple[0]
		self.y = starting_x_y_tuple[1]
		self.value = starting_value
		self.direction = direction_tuple

	# Advance the scanner along its direction
	def advance(self):
		self.x += self.direction[0]
		self.y += self.direction[1]
		
def determine_winner(scanner_manager):
	# We only need to iterate over the scanners consecutive_value_win_condition-1 times
	for turn in range(consecutive_value_win_condition-1):
		scanner_manager.advance_all_scanners()
		# If we have removed all scanners, it is impossible to have a winner
		if not len(scanner_manager.scanners):
			return

	# Return the first of the remaining scanners after we're done iterating
	for scanner_key, scanner in scanner_manager.scanners.iteritems():
		return scanner

def setup_scanners():
	scanner_manager = ScannerManager(board)
	# Start a horizontal scanner at all locations it would be possible to check consecutive_value_win_condition 
	#	spaces in a row without going out of bounds on the right-most edge
	for row in range(len(board)):
		for col in range(len(board[0])-consecutive_value_win_condition+1):
			# print row, col, "HORIZONTAL_DIRECTION_TUPLE"
			scanner_manager.add_scanner((row,0), HORIZONTAL_DIRECTION_TUPLE)

	# Start a vertical scanner at all locations it would be possible to check consecutive_value_win_condition 
	# 	spaces without going out of bounds on the bottom edge
	for row in range(len(board)-consecutive_value_win_condition+1):
		for col in range(len(board[0])):
			# print row, col, "VERTICAL_DIRECTION_TUPLE"
			scanner_manager.add_scanner((0,col), VERTICAL_DIRECTION_TUPLE)

	# Start an ascending scanner at all locations it would be possible to check consecutive_value_win_condition 
	#	spaces without going out of bounds on the right-most edge horizontally, and the bottom edge vertically
	for row in range(len(board)-consecutive_value_win_condition+1):
		for col in range(len(board[0])-consecutive_value_win_condition+1):
			# print row, col, "DESCENDING_DIAGONAL_DIRECTION_TUPLE"
			scanner_manager.add_scanner((row,col), DESCENDING_DIAGONAL_DIRECTION_TUPLE)

	# Start an ascending scanner at all locations it would be possible to check consecutive_value_win_condition 
	#	spaces without going out of bounds on the right-most edge horizontally, and the top edge vertically
	for row in range(len(board)-1,consecutive_value_win_condition-2, -1):
		for col in range(len(board[0])-consecutive_value_win_condition+1):
			# print row, col, "ASCENDING_DIAGONAL_DIRECTION_TUPLE"
			scanner_manager.add_scanner((row,col), ASCENDING_DIAGONAL_DIRECTION_TUPLE)

	return scanner_manager

def main():
	print "Your board:"
	for row in board:
		print " ".join([space if space else "" for space in row])
	print
	scanner_manager = setup_scanners()

	winner = determine_winner(scanner_manager)

	if winner and isinstance(winner, Scanner):
		print "%s Won!" % winner.value.upper()
	else:
		print "Draw!"

if __name__ == "__main__":
	main()
