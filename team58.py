import sys
import random
import signal
import time
import copy
from random import randint

class Player58:
	def __init__(self):
		self.infinity = 99999999
		self.ninfinity = -99999999
		self.next_move = (0, 0)
		self.symbol = 'x'
		self.value = [1 , 10 , 100 , 1000]


	def evaluation(self, board, old_move):
		# return randint(-1000,1000)
		# return 1
		value = 0
		flg = -1
		
		for k in range(2):
			for x in range(0,9,3):
				for y in range(0,9,3):
					flag = -1
					local = 0
					# For Rows
					for i in range(3):
						countx = 0
						counto = 0
						countd = 0
						for j in range(3):
							if board.big_boards_status[k][x+i][y+j] == '-':
								countd += 1
							if board.big_boards_status[k][x+i][y+j] == 'o':
								counto += 1
							if board.big_boards_status[k][x+i][y+j] == 'x':
								countx += 1
						if countx == 3:
							local = self.value[countx]
							flag = 1
							break
						elif counto == 3:
							local = -self.value[countx]
							flag = 1
							break
						else:
							local += self.value[countx]	
					if flag == 1:
						value += local
						continue

					# For Coloumns
					for j in range(3):
						countx = 0
						counto = 0
						countd = 0
						for i in range(3):
							if board.big_boards_status[k][x+i][y+j] == '-':
								countd += 1
							if board.big_boards_status[k][x+i][y+j] == 'o':
								counto += 1
							if board.big_boards_status[k][x+i][y+j] == 'x':
								countx += 1
						if countx == 3:
							local = self.value[countx]
							flag = 1
							break
						elif counto == 3:
							local = -self.value[countx]
							flag = 1
							break
						else:
							local += self.value[countx]
					if flag == 1:
						value += local
						continue

					# For Diagonals
					countx = 0
					counto = 0
					countd = 0
					for i in range(3):
						if board.big_boards_status[k][x+i][y+i] == '-':
							countd += 1
						if board.big_boards_status[k][x+i][y+i] == 'o':
							counto += 1
						if board.big_boards_status[k][x+i][y+i] == 'x':
							countx += 1
					if countx == 3:
						local = self.value[countx]
						flag = 1
					elif (counto == 3):
						local = -self.value[countx]
						flag = 1
					else:
						local += self.value[countx]
					if flag == 1:
						value += local
						continue


					countx = 0
					counto = 0
					countd = 0
					for i in range(3):
						if board.big_boards_status[k][x+i][y+2-i] == '-':
							countd += 1
						if board.big_boards_status[k][x+i][y+2-i] == 'o':
							counto += 1
						if board.big_boards_status[k][x+i][y+2-i] == 'x':
							countx += 1
					if countx == 3:
						local = self.value[countx]
						flag = 1
					elif counto == 3:
						local = -self.value[countx]
						flag = 1
					else:
						local += self.value[countx]
					
					value += local
		return value	


	
	
	def move(self, board, old_move, flag):
		self.symbol = flag
		utility = self.minimax_search(board, old_move, 0, self.ninfinity, self.infinity, True, flag)
		return (self.next_move[0], self.next_move[1], self.next_move[2])

	def minimax_search(self, board, old_move, depth, alpha, beta, max_player, flag):
		status = board.find_terminal_state();
		if depth == 3 or status[0] != 'CONTINUE':
			if self.symbol == 'x':
				return (self.evaluation(board, old_move))
			else:
				return (0 - self.evaluation(board, old_move))

		if max_player:
			value = self.ninfinity
			valid_moves = board.find_valid_move_cells(old_move)
			random.shuffle(valid_moves)
			for move in valid_moves:
				board.update(old_move, move, flag)
				if flag == 'x':
					next_flag = 'o'
				else:
					next_flag = 'x'
				child_value = self.minimax_search(board, move, depth + 1, alpha, beta, False, next_flag)
				
				board.big_boards_status[move[0]][move[1]][move[2]] = '-';
				board.small_boards_status[move[0]][move[1] / 3][move[2] / 3] = '-'

				if child_value > value:
					value = child_value
					if depth == 0:
						self.next_move = copy.deepcopy(move)
				alpha = max(alpha, value)				
				if beta <= alpha:
					break
			# return value
		else:
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
				
				board.big_boards_status[move[0]][move[1]][move[2]] = '-';
				board.small_boards_status[move[0]][move[1] / 3][move[2] / 3] = '-'
				
				if child_value < value:
					value = child_value
					if depth == 0:
						self.next_move = copy.deepcopy(move)
				beta = min(beta, value)				
				if beta <= alpha:
					break
		return value