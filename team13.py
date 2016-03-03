#python
from evaluator_code import *

class Player13:
    def __init__(self):
        self.flag='X'
        self.opponentFlag='O'
        self.alpha=-1e10    #-infinity
        self.beta=1e10      #+infinity
        self.winningCombinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.blockHeuristic = [0]*9
        #self.blockWinBonus = 100
        #Advantage of outside heuristic
        self.outerBlockWeight = 100
        self.middleCellBonus = 5
        self.heuristicMatrix = [[0,-10,-100,-1000],[10,0,0,0],[100,0,0,0],[1000,0,0,0]]
        self.nodeCount=0

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
                if(blockStat[4]=='-'):
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


    def calcBlockHeuristic(self, block_no, boardStat,flag):
        row=(block_no/3)*3
        col=(block_no%3)*3
        gameCellMap = []

        xList = []
        for r in range(row,row+3):
            for c in range(col,col+3):
                xList.append([r,c])
        H = 0
        #Calculate Heuristics for a board
        for i in range(8):
            player = opponent = blank = bonus = 0
            #Calculate Heuristic in a line from all possible winning sequences:
            for j in range(3):
                rowNo = xList[self.winningCombinations[i][j]][0]
                colNo = xList[self.winningCombinations[i][j]][1]
                
                #if the cell has ME
                if boardStat[rowNo][colNo] == flag:
                    player+=1 #No of players in the line
                    
                    #If players have won the same number of blocks, the player with more number of center cells will gain 2 points
                    if rowNo and colNo in (1,4,7):
                        bonus+=self.middleCellBonus
                
                elif boardStat[rowNo][colNo] == '-':
                    blank+=1 #No of blanks in the linefinal
                
                else:
                    opponent+=1 #No of opponents in the line

            #Small Board Win Condition
            '''if player == 3:
                bonus = self.blockWinBonus
                winFlag = True
                
            if opponent == 3:
                bonus = -self.blockWinBonus'''

            H += self.heuristicMatrix[player][opponent]
        return H

    def calcCellHeuristic(self, block_no, boardStat,flag,move):
        row=(block_no/3)*3
        col=(block_no%3)*3
        x=move[0]-row
        y=move[1]-col
        local_blockNo=3*x+y
        finalHeuristic=0
        wins = losses = blanks = 0

        for combination in self.winningCombinations:
        	if wins==3 or losses==3:
        			break
        	for j in combination:
        		heuristic=0
        		if j == local_blockNo:
        			
        			for k in combination:
        				wins = losses = blanks = 0
        				if boardStat[row+(k/3)][col+(k%3)] == flag:
        					wins+=1
        					if k == 4:	#Middle cell bonus
        						heuristic += 20
        				elif boardStat[row+(k/3)][col+(k%3)] == '-':
        					blanks+=1
        				else:
        					losses+=1
        			



        			if wins==3:
        				heuristic+=1000
        				break
        			elif losses==3:
        				heuristic-=1000
        				break
        			if (wins!=0 and losses!=0):
        				break
        			heuristic += 10**wins + 10**blanks -10**losses
        			break
        	finalHeuristic +=heuristic
        return finalHeuristic

    def utility(self, boardStat, blockStat, move, flag):
        block_no = (move[0]/3) * 3 + move[1]/3
        finalHeuristic = 0
        finalHeuristic = self.calcCellHeuristic(block_no,boardStat,flag, move)

        #Heuristics based on the overall blocks' status in the bigger 3x3 gri
        wins = losses = blanks = 0
        heuristic=0
        for combination in self.winningCombinations:
        	if wins==3 or losses==3:
        			break
        	for j in combination:
        		heuristic=0
        		if j == block_no:
        			
        			for k in combination:
        				wins = losses = blanks = 0
        				if blockStat[k] == flag:
        					wins+=1
        				elif blockStat[k] == '-':
        					blanks+=self.calcBlockHeuristic(k, boardStat,flag)
        				else:
        					losses+=1
        			

        			if wins==3:
        				heuristic+=1e10
        				break
        			elif losses==3:
        				heuristic-=1e10
        				break
        			if (wins!=0 and losses!=0):
        				break
        			heuristic += 10*wins + blanks -10*losses
        			break

        opponent_blocksAllowed=self.getAllowedblocks(move, blockStat)
        for i in opponent_blocksAllowed:
        	heuristic-=self.calcBlockHeuristic(i, boardStat,self.getOpponentFlag(flag))

        return finalHeuristic+heuristic

    def terminalUtility(self, boardStat):
        bonus = 0
        #Calculate Heuristics for a board
        for i in self.winningCombinations:
            player = opponent = 0
            
            #Calculate Heuristic in a line from all possible winning sequences:
            for j in i:
                #if the cell has ME
                if boardStat[j] == self.flag:
                    player+=1 #No of players in the line
                                    
                elif boardStat[j] == self.opponentFlag(self.flag):
                    opponent+=1 #No of opponents in the line
        
            #Board Win Condition
            if player == 3:
                bonus = 1e10
                return bonus
            #Board Lose Condition    
            if opponent == 3:
                bonus = -1e10
                return bonus
        return bonus



    def getOpponentFlag(self, flag):
        if flag=='x':
            return 'y'
        elif flag=='X':
            return 'Y'
        elif flag=='y':
            return 'x'
        elif flag=='Y':
            return 'X'

    def isTerminal(self, blockStat):
        for i in xrange(0, 9):
            if blockStat[i] == '-':
                return False
        return True


    def updateBoardStat(self, boardStat, blockStat, move, flag):

        boardStat[move[0]][move[1]] = flag
        block_no = (move[0]/3) * 3 + move[1]/3
        row = (block_no/3) * 3
        col = (block_no%3) * 3
        is_done = 0
        if blockStat[block_no] == '-':
            if boardStat[row][col] == boardStat[row+1][col+1] and boardStat[row+1][col+1] == boardStat[row+2][col+2] and boardStat[row][col] != '-':
                is_done = 1
            if boardStat[row+2][col] == boardStat[row+1][col+1] and boardStat[row+1][col+1] == boardStat[row][col+2] and boardStat[row+1][col+1] != '-':
                is_done = 1
            if not is_done:
                for i in xrange(col, col + 3):
                    if boardStat[row][i] == boardStat[row+1][i] and boardStat[row+1][i] == boardStat[row+2][i] and boardStat[row][i] != '-':
                        is_done = 1
                        break
            if not is_done:
                for i in xrange(row, row + 3):
                    if boardStat[i][col] == boardStat[i][col+1] and boardStat[i][col+1] == boardStat[i][col+2] and boardStat[i][col] != '-':
                        is_done = 1
                        break
            if is_done:
                blockStat[block_no] = flag
            empty_cells = []
            for i in xrange(row, row + 3):
                for j in xrange(col, col + 3):
                    if boardStat[i][j] == '-':
                        empty_cells.append((i, j))
            if len(empty_cells) == 0 and not is_done:
                blockStat[block_no] = 'D'

            #While updating movem if block is conquered, we dont need to go further..so, send a flag
            if (len(empty_cells) == 0 and not is_done) or is_done==1:
                return 1

        return 0

    #Minimax using alpha-beta pruning
    def makeMove(self, boardStat, blockStat, move, flag, depth, alpha, beta):
        board=boardStat[:]
        block=blockStat[:]
        
        check_conqueredBlock=self.updateBoardStat(board,block, move, flag)

        if self.isTerminal(blockStat)==True:
            util = self.terminalUtility(boardStat)
            return util, util    #Return alpha=beta=util

        #If block is conquered before reaching depth
        if depth==2:
            util = self.utility(boardStat, blockStat, move, flag)
            return util,util  #Return alpha=beta=util

        blocksAllowed=self.getAllowedblocks(move,block)
        children=self.getEmptyCells(board, blocksAllowed, block)

        #Maximiser
        if flag==self.flag:
            for child in children:
                copy_board=board[:]
                copy_block=block[:]
                temp_alpha, temp_beta=self.makeMove(copy_board, copy_block, child, self.opponentFlag, depth+1, alpha,beta)
                boardStat[child[0]][child[1]]='-'
                if temp_alpha>temp_beta:	#temp_alpha<temp_beta ensures it is taking from a valid child
                	continue;
                # implementing alpha=max(beta of children)
                if temp_beta>alpha:        
                    alpha=temp_beta
                    if alpha>beta:
                        break
        #Minimiser
        elif flag==self.opponentFlag:
            for child in children:
                copy_board=board[:]
                copy_block=block[:]
                temp_alpha, temp_beta=self.makeMove(copy_board, copy_block, child, self.flag, depth+1, alpha,beta)
                boardStat[child[0]][child[1]]='-'
                if temp_alpha>temp_beta:
                	continue
                #Implementing beta=min(all child alphas)
                if beta>temp_alpha:        #temp_alpha<temp_beta ensures it is taking from a valid child
                    beta=temp_alpha
                    if alpha>beta:
                        break
        return alpha, beta

    def move(self, boardStat, blockStat, oldMove, flag):
        #Get Opponent flag
        print "ensures"
        self.flag=flag;
        self.opponentFlag=self.getOpponentFlag(self.flag)

        blocksAllowed=self.getAllowedblocks(oldMove, blockStat)
        
        #Get list of empty valid cells
        cells = self.getEmptyCells(boardStat, blocksAllowed, blockStat)

        #Incase of first move, play in the center most cell
        if oldMove[0]==-1 and oldMove[1]==-1:
            return (4,4)
        
        #Make copy of Board and Block to avoid mutation 
        alpha=self.alpha
        beta=self.beta

        bestMove=cells[random.randrange(len(cells))]    #In case bestMove does not get referenced in minimax
        self.nodeCount=0;
        val = -1e10
        depth = 1
       	for cell in cells:
       		copy_board=boardStat[:]     #Copy by Value, not reference
           	copy_block=blockStat[:]
           	temp_alpha, temp_beta=self.makeMove(copy_board, copy_block, cell, self.opponentFlag, depth, alpha, beta)
           	boardStat[cell[0]][cell[1]]='-'
           	if temp_alpha>temp_beta:
           		continue
           	if temp_beta>alpha:       #temp_alpha<temp_beta ensures it is taking from a valid child
           	    alpha=temp_beta
           	    if alpha<=beta:
           	        bestMove=cell
           	    else:
           	    	break

        print "Player13:", flag
        return tuple(bestMove)

if __name__ == '__main__':
    obj = Player13()
    game_board, block_stat = get_init_board_and_blockstatus()

