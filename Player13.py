#python
from evaluator_code import *

class Player13:
	def __init__(self):
		pass

	def getEmptyCells(gameBoard, blocksAllowed, boardStat):
		cells = []
		for block in range(blocksAllowed):
			i=block/3
			j=block%3
			m=(j*3)
			for k in range(i*3,i*3+3):
				for l in range(3):
					if(gameBoard[k][m] == '-'):
						cells.append(gameBoard[k][m])
					m+=1
				m+=7

		if cells == []:
			block = [0,1,2,3,4,5,6,7,8]
		for block in range(blocksAllowed):
			i=block/3
			j=block%3
			m=(j*3)
			for k in range(i*3,i*3+3):
				for l in range(3):
					if(gameBoard[k][m] == '-'):
						cells.append(gameBoard[k][m])
					m+=1
				m+=7
		return cells


	def move(self, temp_board, temp_block, old_move, flag):
		#List of permitted blocks, based on old move.
		blocks_allowed  = determine_blocks_allowed(old_move, temp_block)
		#Get list of empty valid cells
		cells = get_empty_out_of(temp_board, blocks_allowed)
		#Choose a move based on some algorithm, here it is a random move.
		print blocks_allowed
		print "\n"
		print cells

if __name__ == '__main__':
	obj = Player13()
	game_board, block_stat = get_init_board_and_blockstatus()
	#print game_board[0][0]
	#print block_stat[0]
	obj.move(game_board,block_stat, (-1,-1), 'x')
