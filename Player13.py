#python
from evaluator_code import *


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

    def utility(self, boardStat, block_stat, oldMove, flag):
        block_no = (oldMove[0]/3) * 3 + oldMove[1]/3
        row=(block_no/3)*3
        col=(block_no%3)*3
        gameCellMap = []

        xList = []
        for r in range(row,row+3):
            for c in range(col,col+3):
                xList.append([r,c])
        print xList

        for i in range(8):
            player = opponent = blank = 0
            for j in range(3):
                rowNo = xList[self.winningCombinations[i][j]][0]
                colNo = xList[self.winningCombinations[i][j]][1]
                if boardStat[rowNo][colNo] == flag:
                    player+=1
                elif boardStat[rowNo][colNo] == '-':
                    blank+=1
                else:
                    opponent+=1
            print player,blank, opponent



    def getOpponentFlag(self, flag):
        if flag=='x':
            return 'y'
        elif flag=='X':
            return 'Y'
        elif flag=='y':
            return 'x'
        elif flag=='Y':
            return 'X'




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
        return





    #Minimax using alpha-beta pruning
    def makeMove(self, boardStat, blockStat, move, flag, depth, alpha, beta):
        board=boardStat[:]
        block=blockStat[:]
        self.updateBoardStat(board,block, move, flag)
        if depth==5:
            util = utility(boardStat, block_stat, oldMove, flag)
            val=random.randrange(100)
            return val, val

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
        print "bestMove is "+str(bestMove)
        return tuple(bestMove)

if __name__ == '__main__':
    obj = Player13()
    game_board, block_stat = get_init_board_and_blockstatus()
    #print game_board[0][0]
    #print block_stat[0]
    obj.move(game_board,block_stat, (4,4), 'x')
    obj.move(game_board,block_stat, (1,2), 'o')

