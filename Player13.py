#python
from evaluator_code import *

playerWorth = 10
opponentWorth = 10
blankWorth = 0
cornerList = [0,2,6,8]
blockWinBonus = 100
inAPatternBonus = 1
middleCellBonus = 5

class blockBounds:
    rowBegin = 1
    rowEnd=1
    colBegin=1
    colEnd=1

class Player13:
    def __init__(self):
        self.flag='X'
        self.opponentFlag='O'
        self.alpha=-1e10    #-infinity
        self.beta=1e10      #+infinity
        self.winningCombinations = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.blockHeuristic = [0]*9
        #self.myStat = ['-']*9


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
        #print "At Block No:",  block_no
        gameCellMap = []

        xList = []
        for r in range(row,row+3):
            for c in range(col,col+3):
                xList.append([r,c])
        H = 0
        #Calculate Heuristics for a board
        winFlag = False
        loseFlag = False
        
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
                        bonus+=middleCellBonus
                
                elif boardStat[rowNo][colNo] == '-':
                    blank+=1 #No of blanks in the line
                
                else:
                    opponent+=1 #No of opponents in the line
            
            #print player,blank, opponent
            
            #Special Conditions for winning and losing because of this move. If there are opponents in the line and hence the line is un-winnable
            if player!=0 and opponent!=0:
                player = 0

            #Small Board Win Condition
            if player == 3:
                bonus = blockWinBonus
                winFlag = True

            H += player*playerWorth + blank*blankWorth - opponent*opponentWorth + bonus
            return H

    def utility(self, boardStat, blockStat, move, flag):
        block_no = (move[0]/3) * 3 + move[1]/3
        #finalHeuristic = self.calcBlockHeuristic(block_no,boardStat,flag)

        #Heuristics based on the overall blocks' status in the bigger 3x3 grid
        posList = [] #posList contains all lines in which the block_no occurs
        for item in self.winningCombinations:
            if block_no in item:
                posList.append(item)
        
        
        weight = 0
        for i in posList:
            #wins = losses = draws = blanks = 0
            for j in i:
                if blockStat[j] == flag:
                    weight+=1000
                                    
                elif blockStat[j] == '-':
                    weight+=self.calcBlockHeuristic(j,boardStat,flag)

                elif blockStat[j] == 'D':
                    weight+=0
                
                else:
                    weight-=1000
        finalHeuristic = weight
        return finalHeuristic


    def getOpponentFlag(self, flag):
        if flag=='x':
            return 'y'
        elif flag=='X':
            return 'Y'
        elif flag=='y':
            return 'x'
        elif flag=='Y':
            return 'X'

    def isTerminal(self, board_stat):
        for i in xrange(0, 9):
            if board_stat[i] == '-':
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

        if self.isTerminal(boardStat)==True:
            util = self.utility(boardStat, blockStat, move, flag)
            return util, util    #Return alpha=beta=util

        if check_conqueredBlock==1:
            util = self.utility(boardStat, blockStat, move, flag)
            return util, util    #Return alpha=beta=util

        #If block is conquered before reaching depth
        if depth==5:
            util = self.utility(boardStat, blockStat, move, flag)
            return util, util    #Return alpha=beta=util

        blocksAllowed=self.getAllowedblocks(move,block)
        children=self.getEmptyCells(board, blocksAllowed, block)

        #Maximiser
        if flag==self.flag:
            for child in children:
                copy_board=board[:]
                copy_block=block[:]
                temp_alpha, temp_beta=self.makeMove(copy_board, copy_block, child, self.opponentFlag, depth+1, alpha,beta)
                boardStat[child[0]][child[1]]='-'
                # implementing alpha=max(beta of children)
                if temp_beta>alpha and temp_alpha<temp_beta:        #temp_alpha<temp_beta ensures it is taking from a valid child
                    alpha=temp_beta
                    if alpha<=beta:
                        bestMove=child
                    else:
                        break
            return alpha, beta
        #Minimiser
        elif flag==self.opponentFlag:
            for child in children:
                copy_board=board[:]
                copy_block=block[:]
                temp_alpha, temp_beta=self.makeMove(copy_board, copy_block, child, self.flag, depth+1, alpha,beta)
                boardStat[child[0]][child[1]]='-'
                #Implementing beta=min(all child alphas)
                if beta>temp_alpha and temp_alpha<temp_beta:        #temp_alpha<temp_beta ensures it is taking from a valid child
                    beta=temp_alpha
                    if alpha<=beta:
                        bestMove=child
                    else:
                        break
            return alpha, beta

    def move(self, boardStat, blockStat, oldMove, flag):


        #Incase of first move, play in the center most cell
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

        bestMove=cells[random.randrange(len(cells))]    #In case bestMove does not get referenced in minimax
        for cell in cells:
            copy_board=boardStat[:]     #Copy by Value, not reference
            copy_block=blockStat[:]
            temp_alpha, temp_beta=self.makeMove(copy_board, copy_block, cell, self.opponentFlag, 1, alpha, beta)
            boardStat[cell[0]][cell[1]]='-'
            if temp_beta>alpha and temp_alpha<=temp_beta:       #temp_alpha<temp_beta ensures it is taking from a valid child
                alpha=temp_beta
                if alpha<=beta:
                    bestMove=cell
                else:
                    break

        #Choose a move based on some algorithm, here it is a random moveself.
        #print "bestMove is "+str(bestMove)
        return tuple(bestMove)

if __name__ == '__main__':
    obj = Player13()
    game_board, block_stat = get_init_board_and_blockstatus()
    #print game_board[0][0]
    #print block_stat[0]
    #move = obj.move(game_board,block_stat, (-1,-1), 'x')
    #update_lists(game_board, block_stat, move, obj.flag)
    #obj.move(game_board,block_stat, (1,2), 'o')

