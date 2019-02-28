import sys
import random
import signal
import time
import copy

class Player48:
	def __init__(self):
		self.infinity = 99999999
		self.ninfinity = -99999999
		self.next_move = (0, 0)
		self.symbol = 'x'



	def evaluation(self, board, old_move):
		# return random(-1000,1000)
		return 1

	def move(self, board, old_move, flag):
		self.symbol = flag
		utility = self.minimax_search(board, old_move, 0, self.ninfinity, self.infinity, True, flag)
		return (self.next_move[0], self.next_move[1])

	def minimax_search(self, board, old_move, depth, alpha, beta, max_player, flag):
		#print "Entered"
		status = board.find_terminal_state();
		#print status
		if depth == 3 or status[0] != 'CONTINUE':
			#return random.randint(0, 1000)
			#return 1
			if self.symbol == 'x':
				return (self.evaluation(board, old_move))
			else:
				return (0 - self.evaluation(board, old_move))

		if max_player:
			#print "Enteredmax"
			value = self.ninfinity
			valid_moves = board.find_valid_move_cells(old_move)
			random.shuffle(valid_moves)
			#print valid_moves
			for move in valid_moves:
				board.update(old_move, move, flag)
				if flag == 'x':
					next_flag = 'o'
				else:
					next_flag = 'x'
				child_value = self.minimax_search(board, move, depth + 1, alpha, beta, False, next_flag)
				
				for k in range(2):		
					board.big_boards_status[k][move[0]][move[1]] = '-';
					board.small_boards_status[k][move[0] / 3][move[1] / 3] = '-'
				if child_value > value:
					value = child_value
					if depth == 0:
						self.next_move = copy.deepcopy(move)
				alpha = max(alpha, value)				
				if beta <= alpha:
					break
			return value

		else:
			#print "Enteredmin"
			value = self.infinity
			valid_moves = board.find_valid_move_cells(old_move)
			random.shuffle(valid_moves)
			for move in valid_moves:
				board.update(old_move, move, flag)
				if flag == 'x':
					next_flag = 'o'
				else:
					next_flag = 'x'
				child_value = self.minimax_search(board, move, depth + 1, alpha, beta, True, next_flag)
				#print "Child ended"
				for k in range(2):	
					board.big_boards_status[k][move[0]][move[1]] = '-';
					board.small_boards_status[k][move[0] / 3][move[1] / 3] = '-'
				if child_value < value:
					value = child_value
					if depth == 0:
						self.next_move = copy.deepcopy(move)
				beta = min(beta, value)				
				if beta <= alpha:
					break
		return value