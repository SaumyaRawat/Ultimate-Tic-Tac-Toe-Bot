#python
from evaluator_code import *

class Player13:
	def __init__(self):
		pass

	def getEmptyCells(self,gameBoard, blocksAllowed, boardStat):
		print "jhf"
			

	def getAllowedblocks(self,oldMove, blockStat):
		# To check block status and get permittedBlocks in which we can make our move
		permittedBlocks=[]
		if oldMove[0]%3==0:

			if oldMove[1]%3==0:
				if(blockStat[1]=='-'):
					permittedBlocks.append(1)
				if(blockStat[3]=='-'):
					permittedBlocks.append(3)

			elif oldMove[1]%3==1:
				if(blockStat[0]=='-'):
					permittedBlocks.append(0)
				if(blockStat[2]=='-'):
					permittedBlocks.append(2)

			elif oldMove[1]%3==2:
				if(blockStat[1]=='-'):
					permittedBlocks.append(1)
				if(blockStat[5]=='-'):
					permittedBlocks.append(5)
			else:
				sys.exit(1)
		elif oldMove[0]%3==1:
			if oldMove[1]%3==0:
				if(blockStat[0]=='-'):
					permittedBlocks.append(0)
				if(blockStat[6]=='-'):
					permittedBlocks.append(6)

			elif oldMove[1]%3==1:
				if(blockStat[0]=='-'):
					permittedBlocks.append(4)

			elif oldMove[1]%3==2:
				if(blockStat[2]=='-'):
					permittedBlocks.append(2)
				if(blockStat[8]=='-'):
					permittedBlocks.append(8)
			else:
				sys.exit(1)
		elif oldMove[0]%3==2:

			if oldMove[1]%3==0:
				if(blockStat[3]=='-'):
					permittedBlocks.append(3)
				if(blockStat[7]=='-'):
					permittedBlocks.append(7)

			elif oldMove[1]%3==1:
				if(blockStat[6]=='-'):
					permittedBlocks.append(6)
				if(blockStat[8]=='-'):
					permittedBlocks.append(8)

			elif oldMove[1]%3==2:
				if(blockStat[7]=='-'):
					permittedBlocks.append(7)
				if(blockStat[5]=='-'):
					permittedBlocks.append(5)
			else:
				sys.exit(1)
		else:
			sys.exit(1)

		return permittedBlocks


	def move(self, boardStat, blockStat, oldMove, flag):
		#List of permitted blocks, based on old move.
		#blocks_allowed  = determine_blocks_allowed(old_move, temp_block)
		if oldMove[0]==-1 and oldMove[1]==-1:
			return (4,4)

		blocksAllowed=self.getAllowedblocks(oldMove, blockStat)
		#Get list of empty valid cells
		#cells = get_empty_out_of(temp_board, blocksAllowed, temp_block)
		#Choose a move based on some algorithm, here it is a random move.
		print blocksAllowed

if __name__ == '__main__':
	obj = Player13()
	game_board, block_stat = get_init_board_and_blockstatus()
	#print game_board[0][0]
	#print block_stat[0]
	obj.move(game_board,block_stat, (6,5), 'x')
