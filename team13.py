#python
from evaluator_code import *

class Player13:
    def __init__(self):
        self.flag='X'
        self.opponentFlag='O'
        self.alpha=-1e10    #-infinity
        self.beta=1e10      #+infinity
        self.winningCombinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.outerBlockWeight = 100 #Advantage of outside board heuristic
        self.middleCellBonus = 5
        self.heuristicMatrix = [[0,-10,-100,-1000],[10,0,0,0],[100,0,0,0],[1000,0,0,0]]

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
        finalHeuristic = H = 0
        wins = losses = blanks = bonus = 0
        row=(block_no/3)*3
        col=(block_no%3)*3
        
        #Contains all (row,col) tuples of this particular board
        xList = []
        for r in range(row,row+3):
            for c in range(col,col+3):
                xList.append([r,c])
        blockBonus = 0
        for combination in self.winningCombinations:
            #if wins==3 or losses==3:
                    #break
            #traversing for all 8 combinations of r,c linewise :
            wins = losses = blanks = bonus = 0
            for j in combination:
                r = xList[j][0]
                c = xList[j][1]
                if boardStat[r][c] == flag:
                    wins+=1
                    if r and c in  (1,4,7):  #Middle cell bonus
                        bonus = self.middleCellBonus
                elif boardStat[r][c] == '-':
                    blanks+=1
                else:
                    losses+=1
            if wins is 1 and losses is 2:
                bonus += 10
            H += self.heuristicMatrix[wins][losses] + bonus
        return H

                
    def utility(self, boardStat, blockStat, move, flag):
        block_no = (move[0]/3) * 3 + move[1]/3
        finalHeuristic = 0
        finalHeuristic = self.calcBlockHeuristic(block_no,boardStat,flag)

        #Heuristics based on the overall blocks' status in the bigger 3x3 grid
        weight = 0
        for i in self.winningCombinations:
            wins = losses = draws = blanks = 0
            for j in i:
                if blockStat[j] == flag:
                    wins+=1
                                    
                elif blockStat[j] == '-':
                    blanks+=1

                elif blockStat[j] == 'D':
                    draws+=1
                
                else:
                    losses+=1
            weight += self.heuristicMatrix[wins][losses]
        finalHeuristic+=(self.outerBlockWeight*weight)
        if finalHeuristic == 1e10:
            print "OH NO!"
        return finalHeuristic

    def terminalUtility(self, blockStat):
        bonus = 0
        #Calculate Heuristics for a board
        for i in self.winningCombinations:
            player = opponent = 0
            
            #Calculate Heuristic in a line from all possible winning sequences:
            for j in i:
                #if the block has ME
                if blockStat[j] == self.flag:
                    player+=1 #No of players in the line
                                    
                elif blockStat[j] == self.opponentFlag(self.flag):
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
        prevBlock='-'
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
            	prevBlock=blockStat[block_no]
                blockStat[block_no] = flag
            empty_cells = []
            for i in xrange(row, row + 3):
                for j in xrange(col, col + 3):
                    if boardStat[i][j] == '-':
                        empty_cells.append((i, j))
            if len(empty_cells) == 0 and not is_done:
            	prevBlock=blockStat[block_no]
                blockStat[block_no] = 'D'

            #While updating movem if block is conquered, we dont need to go further..so, send a flag
            return prevBlock, block_no

    def makeMove(self, boardStat, blockStat, move, flag, depth, alpha, beta):
        board=boardStat[:]
        block=blockStat[:]

        #if self.isTerminal(blockStat)==True:
            #util = self.terminalUtility(blockStat)
            #return util, util    #Return alpha=beta=util

        #If block is conquered before reaching depth
        if depth==8:
            util = self.utility(board, block, move, flag)
            return util  #Return alpha=beta=util

        blocksAllowed=self.getAllowedblocks(move,block)
        children=self.getEmptyCells(board, blocksAllowed, block)

        #Maximiser
        if flag==self.flag:
        	value = -1e10
        	for child in children:
        		if alpha>=beta:
        			break
                f,b_no=self.updateBoardStat(board,block, child, self.flag)
                value=max(value,self.makeMove(board, block, child, self.opponentFlag, depth+1, alpha,beta))
                alpha=max(value, alpha)
                board[child[0]][child[1]]='-'
                block[b_no]=f

        #Minimiser
        elif flag==self.opponentFlag:
        	value = 1e10
        	for child in children:
        		if alpha>=beta:
        			break
                f,b_no=self.updateBoardStat(board,block, child, self.opponentFlag)
                value=min(value, self.makeMove(board, block, child, self.flag, depth+1, alpha,beta))
                beta=min(value, beta)
                board[child[0]][child[1]]='-'
                block[b_no]=f
            
        return value
       # print str(depth)+str(" ")+str(alpha)+str(" ")+str(beta)

    def move(self, boardStat, blockStat, oldMove, flag):
        #Get Opponent flag
        self.flag=flag;
        self.opponentFlag=self.getOpponentFlag(self.flag)

        blocksAllowed=self.getAllowedblocks(oldMove, blockStat)
        
        #Get list of empty valid cells
        cells = self.getEmptyCells(boardStat, blocksAllowed, blockStat)

        #Incase of first move, play in the center most cell
        if oldMove[0]==-1 and oldMove[1]==-1:
            return (4,4)
            #return cells[random.randrange(len(cells))]
        
        #Make copy of Board and Block to avoid mutation 
        alpha=self.alpha
        beta=self.beta

        #In case bestMove does not get referenced in minimax
        depth = 1
        bestMove = []
        value = -1e10
        bestVal = -1e15
        for cell in cells:
            copy_board=boardStat[:]     #Copy by Value, not reference
            copy_block=blockStat[:]
            self.updateBoardStat(copy_board,copy_block, cell, self.flag)
            value=self.makeMove(copy_board, copy_block, cell, self.flag, depth, alpha, beta)
            boardStat[cell[0]][cell[1]]='-'
            if value>bestVal:
            	print value
            	bestMove=[]
            	bestMove.append(tuple(cell))
            	bestVal=value
            elif value == bestVal:
            	bestMove.append(tuple(cell))

        if len(bestMove)==0:
            bestMove.append(cells[random.randrange(len(cells))])
            print "It was 0"

        print "Player13:", flag
        print "Heur:", bestVal
        return bestMove[random.randrange(len(bestMove))]

if __name__ == '__main__':
    obj = Player13()
    game_board, block_stat = get_init_board_and_blockstatus()
