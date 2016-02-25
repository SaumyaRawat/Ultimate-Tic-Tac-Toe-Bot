#python
from evaluator_code import *

class Player13:
	def __init__(self):
		self.flag='X'
		self.opponentFlag='O'
		self.alpha=-1e10	#-infinity
		self.beta=1e10		#+infinity
		self.winningCombinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

	def getEmptyCells(self, gameBoard, blocksAllowed, blockStat):
		cells = []
		for block in blocksAllowed:
			i=block/3
			j=block%3
			for k in range(i*3,i*3+3):
				for l in range(j*3,j*3+3):
					if(gameBoard[k][l] == '-'):
						cells.append((k,l))

		if cells == []:
			block = [0,1,2,3,4,5,6,7,8]
			blocksAllowed = []
			for i in block:
				if blockStat[i]=='-':
					blocksAllowed.append(i)

			for block in blocksAllowed:
				i=block/3
				j=block%3
				for k in range(i*3,i*3+3):
					for l in range(j*3,j*3+3):
						if(gameBoard[k][l] == '-'):
							cells.append((k,l))

		return cells

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

	def getOpponentFlag(self, flag):
		if flag=='x':
			return 'y'
		elif flag=='X':
			return 'Y'
		elif flag=='y':
			return 'x'
		elif flag=='Y':
			return 'X'

	def utility(self, boardStat, block_stat, oldMove, flag):
		block_no = (oldMove[0]/3) * 3 + oldMove[1]/3


	def makeMove(self, boardStat, blockStat, oldMove, flag, depth, alpha, beta):
		if depth==4:
			val=self.utility(boardStat, blockStat)
			return val, val, val, oldMove
		return 1,2,3,(4,5)

	def move(self, boardStat, blockStat, oldMove, flag):
		#List of permitted blocks, based on old move.
		if oldMove[0]==-1 and oldMove[1]==-1:
			return (4,4)

		#Get Opponent flag
		self.flag=flag;
		self.opponentFlag=self.getOpponentFlag(self.flag)

		blocksAllowed=self.getAllowedblocks(oldMove, blockStat)
		
		#Get list of empty valid cells
		cells = self.getEmptyCells(boardStat, blocksAllowed, blockStat)
		
		#Make copy of Board and Block to avoid mutation 
		alpha=self.alpha
		beta=self.beta
		copy_board=boardStat
		copy_block=blockStat
		for cell in cells:
			alpha, beta, value, bestMove=self.makeMove(copy_board, copy_block, cell, self.opponentFlag, 1, alpha, beta)
			
	
		return cells[random.randrange(len(cells))]

		#Choose a move based on some algorithm, here it is a random move.


if __name__ == '__main__':
	obj = Player13()
	game_board, block_stat = get_init_board_and_blockstatus()
	#print game_board[0][0]
	#print block_stat[0]
	obj.move(game_board,block_stat, (2,2), 'x')
