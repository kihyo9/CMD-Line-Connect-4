import sys
from sys import stdout
import time
import random
import copy

rowNum = 6
colNum = 7

game_board = [['_' for _ in range(colNum)] for _ in range(rowNum)]

def main1(level):

	# who goes first?
	turn = 0
	pieces = ['x','o']
	human = flipcoin()
	if human == 1:
		print("Computer moves first!")
	else:
		print("Human moves first!")
	time.sleep(1.5)

	# game
	while turn < 42:
		player = (turn % 2)
		printboard(game_board)	

		# take input
		if player == human:
			print('Human turn (' + pieces[player] + ')...')
			validInput = False
			while not validInput:
				col = input('Choose a column (1-7): ')
				if col not in ['1','2','3','4','5','6','7']:
					print('Invalid input!')
					continue
				if not updateboard(game_board, int(col),pieces[player]):
					print('Column is full!')
					continue
				validInput = True
		else:
			# fake thinking...
			for _ in range(1):
				for i in range(4):
					dots = '' + i*'.' + (4-i)*' '
					stdout.write('\rComputer turn (' + pieces[player] + ')' + dots)
					stdout.flush()
					time.sleep(0.2)
			stdout.write('\n')

			# computer AI choice
			choice = 0
			if level == '1':
				choice = connect4AI()
			elif level == '2':
				choice = connect4AI2(game_board, pieces[player],pieces[player-1],block=True)
			elif level == '3':
				analysis_depth = 5
				strat = 'net'
				start = 1 # a change for 'start' requires changing in the connect4AI3() function below
				choice = connect4AI3_helper(copy.deepcopy(game_board), pieces[player],pieces[player-1], analysis_depth, strat, start)
			print('Computer chose column ' + str(choice))
			updateboard(game_board, choice,pieces[player])

		# evaluate
		status = evaluateboard(game_board)
		if status == '_':
			pass
		elif status == 'x':
			winner = 'Human' if human == 0 else 'Computer'
			print('\n\n' + winner + ' wins!')
			break
		elif 'o':
			winner = 'Human' if human == 1 else 'Computer'
			print('\n\n' + winner + ' wins!')
			break
		if turn == 41:
			print('\n\nBoard == full... draw!')
		turn += 1

	printboard(game_board)
	print('\nEnd of game!')

def main2():

	# play
	turn = 0
	pieces = ['x','o']

	while turn < 42:

		printboard(game_board)

		player = (turn % 2)
		print('Player ' + str(player+1) + '\'s turn (' + pieces[player] + ')...')

		# take input
		validInput = False
		while not validInput:
			col = input('Choose a column (1-7): ')
			if col not in ['1','2','3','4','5','6','7']:
				print('Invalid input!')
				continue

			if not updateboard(game_board, int(col),pieces[player]):
				print('Column == full!')
				continue

			validInput = True


		# evaluate
		status = evaluateboard(game_board)
		if status == '_':
			pass
		elif status == 'x':
			print('\n\nPlayer 1 wins!')
			break
		elif 'o':
			print('\n\nPlayer 2 wins!')
			break

		if turn == 41:
			print('\n\nBoard == full... draw!')

		turn += 1

	printboard(game_board)
	print('\nEnd of game!')


def printboard(board):
	print('\n')
	for i in range(rowNum):
		row = board[rowNum - i - 1]
		for piece in row:
			print('|',end=piece)
		print('|')

	print('',end='|')
	for i in range(colNum):
		print(str(i+1),end='|')
	print('')

def updateboard(board, column, piece):
	for row in board:
		if row[column-1] == '_':
			row[column-1] = piece
			return True
	return False

def evaluateboard(board):
	rowsx = [set() for _ in range(rowNum)]	
	diagsx1 = [set() for _ in range(rowNum)]
	diagsx2 = [set() for _ in range(rowNum)]

	rowso = [set() for _ in range(rowNum)]
	diagso1 = [set() for _ in range(rowNum)]
	diagso2 = [set() for _ in range(rowNum)]

	# eval for row win
	for i,row in enumerate(board):
		count = 0
		prevPiece = ''
		first = True
		for j,piece in enumerate(row):
			# add to sets
			if piece == '_':
				count = 0
				prevPiece = piece
				continue
			elif piece == 'x':
				rowsx[i].add(j)
				diagsx1[i].add(j+i)
				diagsx2[i].add(j-i)
			elif piece == 'o':
				rowso[i].add(j)
				diagso1[i].add(j+i)
				diagso2[i].add(j-i)

			# keep track of previous piece in row
			if first:
				prevPiece = piece
				first = False
				continue
			if prevPiece == piece:
				count += 1
			else:
				count = 0

			# update previous piece
			prevPiece = piece

			# winning condition
			if count >= 3:
				return prevPiece

	# eval for col win - any shared col position in 4 consecutive rows
	for i in range(rowNum - 3):
		setx = rowsx[i] & rowsx[i+1] & rowsx[i+2] & rowsx[i+3]
		seto = rowso[i] & rowso[i+1] & rowso[i+2] & rowso[i+3]

		if len(setx) != 0:
			return 'x'
		elif len(seto) != 0:
			return 'o'

	# eval diagonals
	for i in range(rowNum - 3):
		setx1 = diagsx1[i] & diagsx1[i+1] & diagsx1[i+2] & diagsx1[i+3]
		setx2 = diagsx2[i] & diagsx2[i+1] & diagsx2[i+2] & diagsx2[i+3]

		seto1 = diagso1[i] & diagso1[i+1] & diagso1[i+2] & diagso1[i+3]
		seto2 = diagso2[i] & diagso2[i+1] & diagso2[i+2] & diagso2[i+3]
		if len(setx1) != 0 or len(setx2) != 0:
			return 'x'
		elif len(seto1) != 0 or len(seto2) != 0:
			return 'o'	

	return '_'

def deletePieceInColumn(board, column):
	for i in range(rowNum):
		row = board[rowNum - i - 1]
		piece = row[column - 1]
		if piece != '_':
			row[column - 1] = '_'
			return True
			break
	return False


def clearboard():
	global game_board 
	game_board =\
	[['_','_','_','_','_','_','_'],\
	['_','_','_','_','_','_','_'],\
	['_','_','_','_','_','_','_'],\
	['_','_','_','_','_','_','_'],\
	['_','_','_','_','_','_','_'],\
	['_','_','_','_','_','_','_']]

def flipcoin():
	print('\nFlipping coin...')
	c = ['\\','|','/','–']
	for _ in range(4):
		for char in c:
			stdout.write('\r' + char)
			stdout.flush()
			time.sleep(0.08)
	stdout.write('\n')
	# return 1
	return random.randint(0, 1)

def connect4AI():
	return random.randint(1, 7)

def connect4AI2(board, piece, piece2, block=False):
	board2 = copy.deepcopy(board)

	# winning p
	p = [[0,0] for _ in range(colNum)]

	for i in range(colNum):
		# play/== column full
		if not updateboard(board2, i+1, piece):
			p[i][0] = -2
			continue

		# == this move a win
		if evaluateboard(board2) == piece:
			p[i][0] += 1
			deletePieceInColumn(board2, i+1)
			return (i+1)

		# opponent's move
		for j in range(colNum):
			# play/== column full
			if not updateboard(board2, j+1, piece2):
				continue

			# == this move a win for opponent
			if evaluateboard(board2) == piece2:
				p[i][0] = -1
				# deletePieceInColumn(board2, i+1)
				# deletePieceInColumn(board2, j+1)
				if block:
					return (j+1)
				else:
					break

			# my move again
			for k in range(colNum):
				# play/== column full
				if not updateboard(board2, k+1, piece):
					continue				

				# == this move a win
				if evaluateboard(board2) == piece:
					p[i][0] += 1
					deletePieceInColumn(board2, k+1)
					break

				# delete my second move
				deletePieceInColumn(board2, k+1)

			p[i][1] += 1

			# delete opponent's move
			deletePieceInColumn(board2, j+1)

		# delete my first move
		deletePieceInColumn(board2, i+1)

	# convert p to a play
	value = -2
	plays = []
	bag = []

	for pair in p:
		if pair[0] > 0:
			plays.append(float(pair[0])/float(pair[1]))
		if pair[0] == -2:
			plays.append(-2)
		if pair[0] == -1:
			plays.append(-1)
		else:
			plays.append(0)

	for i,play in enumerate(plays):
		if play > value:
			bag.clear()
			bag.append(i+1)
			value = play
		elif play == value:
			bag.append(i+1)

	return random.choice(bag)

# input a deepcopy of the original game_board state
def connect4AI3(board, piece, piece2, analysis_depth, start):
	# winning p
	p = [0 for _ in range(colNum)]

	for i in range(colNum):
		# play/is column full
		if not updateboard(board, i+1, piece):
			p[i] = -1
			continue
		# this move a win
		elif evaluateboard(board) == piece:
			if (start % 2) == 1: # change if start default is changed
				p[i] = [1., 0.]
			else:
				p[i] = [0., 1.]
		else:
			if start < analysis_depth:
				# switch pieces so subsequent recursion stacks switch sides for the opponent's move
				p[i] = connect4AI3(board, piece2, piece, analysis_depth, start+1)
			else:
				p[i] = [0., 0.]

		# delete simulated move
		deletePieceInColumn(board, i+1)

	# aggregate results, but not for the first stack
	if start > 1: # change if start default is changed
		combined = [0., 0.]
		count = 0

		for prob in p:
			if prob != -1:
				count += 1
				combined[0] += prob[0]
				combined[1] += prob[1]

		for i in range(2):
			combined[i] /= count

		return combined
	else:
		return p

def connect4AI3_helper(board, piece, piece2, analysis_depth, strat, start):
	probs = connect4AI3(board, piece, piece2, analysis_depth, start)

	# win
	choice = []
	choice2 = []
	if strat == 'win':
		value = 0.
		for i in range(colNum):
			if probs[i] == -1:
				continue
			if probs[i][0] > value:
				value = probs[i][0]
				choice = []
				choice.append(i+1)
			elif probs[i][0] == value:
				choice.append(i+1)
		value = 1
		for c in choice:
			if probs[c-1] == -1:
				continue
			if probs[c-1][1] < value:
				value = probs[c-1][1]
				choice2 = []
				choice2.append(c)
			elif probs[i][1] == value:
				choice2.append(c)					
	# not lose
	elif strat == 'not lose':
		value = 1.
		for i in range(colNum):
			if probs[i] == -1:
				continue
			if probs[i][1] < value:
				value = probs[i][1]
				choice = []
				choice.append(i+1)
			elif probs[i][1] == value:
				choice.append(i+1)
		value = 0
		for c in choice:
			if probs[c-1] == -1:
				continue
			if probs[c-1][0] > value:
				value = probs[c-1][0]
				choice2 = []
				choice2.append(c)
			elif probs[i][0] == value:
				choice2.append(c)
	# net percentage
	elif strat == 'net':
		win_weight = 1.
		loss_weight = 1.
		value = -2.
		for i in range(colNum):
			if probs[i] == -1:
				continue
			if win_weight*probs[i][0] - loss_weight*probs[i][1] > value:
				value = win_weight*probs[i][0] - loss_weight*probs[i][1]
				choice2 = []
				choice2.append(i+1)
			elif win_weight*probs[i][0] - loss_weight*probs[i][1] == value:
				choice2.append(i+1)

	# 4 is the most likely to be played, with probabilities decreasing as the number's distance from 4 increases
	choice3 = []
	for i in range(colNum):
		if (i+1) in choice2:
			for _ in range(4-abs((i+1)-4)):
				choice3.append(i+1)

	# printprobs(probs) # for seeing what the computer think

	return random.choice(choice3)

def printprobs(probs):
	for i, move in enumerate(probs):
		print("{}. {:0.3f}/{:0.3f} ".format(i+1, move[0], move[1]),end='')
	print('')


if __name__ == '__main__':
	print("\n*****************************************")
	print("*** Welcome to Cmd-Line Connect Four! ***")
	print("*****************************************\n")

	again = True
	while again:
		clearboard()

		p = input('Enter number of players (1/2): ')
		while(p not in ['1','2']):
			p = input('Invalid input, enter again: ')

		if p == '1':
			level = input('Enter computer AI level (1, 2 or 3): ')
			while(level not in ['1','2','3']):
				level = input('Invalid input, enter again: ')			
			main1(level)
		elif p == '2':
			main2()
		else:
			x = input("Something went wrong! Press enter to exit... ")
			sys.exit()

		a = input('Play again (y/n)? ')
		again = (a == 'y')