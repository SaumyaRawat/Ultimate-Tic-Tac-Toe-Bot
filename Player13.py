#python
from evaluator_code import *

class Player13:
	def __init__(self):
		pass

	def getEmptyCells(gameBoard, blocksAllowed, boardStat):

		int i,j,block;
		for block in range(blocksAllowed):
			

	def move(self, board, block, old_move, flag):
		#List of permitted blocks, based on old move.
		blocks_allowed  = determine_blocks_allowed(old_move, temp_block)
		#Get list of empty valid cells
		cells = get_empty_out_of(temp_board, blocks_allowed)
		#Choose a move based on some algorithm, here it is a random move.
		print blocks_allowed
		print cells

obj = Player13()

