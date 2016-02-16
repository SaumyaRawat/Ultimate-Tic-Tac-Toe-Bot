class Player1:
	
	def __init__(self):
		# You may initialize your object here and use any variables for storing throughout the game
		pass

	def move(self,temp_board,temp_block,old_move,flag):
		#List of permitted blocks, based on old move.
		blocks_allowed  = determine_blocks_allowed(old_move, temp_block)
		#Get list of empty valid cells
		cells = get_empty_out_of(temp_board, blocks_allowed)
		#Choose a move based on some algorithm, here it is a random move.
		return cells[random.randrange(len(cells))]