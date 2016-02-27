import random
import copy

inf = 1e6

class Player14(object):

    def __init__(self):
        self.inf = 1e10
        self.generateHeuristicMatrix()

    def move(self, current_board_game, board_stat, move_by_opponent, flag):
        if move_by_opponent == (-1, -1):
            return (4, 4)
        self.myMark = flag
        self.other = self.getOpp(self.myMark)
        possible_cells = self.getValidCells(current_board_game, board_stat, move_by_opponent)
        self.node_count = 0
        idx = possible_cells[0]
        best_val = -self.inf
        depth = 0
        while best_val != inf and self.node_count < 100000:
            depth += 1
            best_val = -self.inf
            for cell in possible_cells:
                bstat = board_stat[:]
                self.updateBoardStat(current_board_game, bstat, cell, flag)
                temp = self.alphaBetaPruning(current_board_game, bstat, depth, -self.inf, self.inf, True, cell)
                if temp > best_val:
                    best_val = temp
                    idx = cell
                current_board_game[cell[0]][cell[1]] = '-'
            my_move = idx
            print "sahay ", flag
            return my_move

    def getOpp(self, flag):
        if flag == 'x':
            return 'o'
        return 'x'

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


#Tan
        row, column = move_by_opponent[0] % 3, move_by_opponent[1] % 3
        valid_blocks = []
        if row == 0 and column == 0:
            valid_blocks = [0, 1, 3]
        elif row == 0 and column == 2:
            valid_blocks = [1, 2, 5]
        elif row == 2 and column == 0:
            valid_blocks = [3, 6, 7]
        elif row == 2 and column == 2:
            valid_blocks = [5, 7, 8]
        else:
            valid_blocks = [3 * row + column]
        valid_cells = []
        for i in valid_blocks:
            if board_stat[i] != '-':
                continue
            row = (i/3) * 3
            column = (i%3) * 3
            for j in xrange(0, 3):
                for k in xrange(0, 3):
                    r = row + j
                    c = column + k
                    if current_board_game[r][c] == '-':
                        valid_cells.append((r, c))
        if len(valid_cells) == 0:
            for i in xrange(0, 9):
                for j in xrange(0, 9):
                    if board_stat[(i/3) * 3 + (j/3)] == '-' and current_board_game[i][j] == '-':
                        valid_cells.append((i, j))
        easy_move = []
        for i in valid_cells:
            if board_stat[(i[0]%3) * 3 + i[1]%3] != '-':
                valid_cells.remove(i)
                easy_move.append(i)
        if len(valid_cells) == 0:
            valid_cells = easy_move
        random.shuffle(valid_cells)
        return valid_cells

    def updateBoardStat(self, board_game, board_stat, move, flag):
        board_game[move[0]][move[1]] = flag
        block_no = (move[0]/3) * 3 + move[1]/3
        row = (block_no/3) * 3
        column = (block_no%3) * 3
        is_done = 0
        if board_stat[block_no] == '-':
            if board_game[row][column] == board_game[row+1][column+1] and board_game[row+1][column+1] == board_game[row+2][column+2] and board_game[row][column] != '-':
                is_done = 1
            if board_game[row+2][column] == board_game[row+1][column+1] and board_game[row+1][column+1] == board_game[row][column+2] and board_game[row+1][column+1] != '-':
                is_done = 1
            if not is_done:
                for i in xrange(column, column + 3):
                    if board_game[row][i] == board_game[row+1][i] and board_game[row+1][i] == board_game[row+2][i] and board_game[row][i] != '-':
                        is_done = 1
                        break
            if not is_done:
                for i in xrange(row, row + 3):
                    if board_game[i][column] == board_game[i][column+1] and board_game[i][column+1] == board_game[i][column+2] and board_game[i][column] != '-':
                        is_done = 1
                        break
            if is_done:
                board_stat[block_no] = flag
            empty_cells = []
            for i in xrange(row, row + 3):
                for j in xrange(column, column + 3):
                    if board_game[i][j] == '-':
                        empty_cells.append((i, j))
            if len(empty_cells) == 0 and not is_done:
                board_stat[block_no] = 'd'
        return
    def getValidCells(self, current_board_game, board_stat, move_by_opponent):
        cells = []
        blocksAllowed = self.getAllowedblocks(move_by_opponent,board_stat)
        cells = self.getEmptyCells(current_board_game, blocksAllowed, board_stat)
        return cells
        
    def alphaBetaPruning(self, board_game, board_stat, depth, alpha, beta, flag, node):
        self.node_count += 1
        if self.isTerminal(board_stat):
            return self.getUtilityVal(board_stat)
        if depth == 0:
            return self.getHeuristicVal(board_game, board_stat)
        children = self.getValidCells(board_game, board_stat, node)
        if flag:
            val = -self.inf
            for child in children:
                new_board_stat = board_stat[:]
                self.updateBoardStat(board_game, new_board_stat, child, self.myMark if flag else self.other)
                val = max(val, self.alphaBetaPruning(board_game, new_board_stat, depth - 1, alpha, beta, False, child))
                alpha = max(alpha, val)
                board_game[child[0]][child[1]] = '-'
                if beta <= alpha:
                    break
            return val
        else:
            val = self.inf
            for child in children:
                new_board_stat = board_stat[:]
                self.updateBoardStat(board_game, new_board_stat, child, myMark if flag else self.other)
                val = min(val, self.alphaBetaPruning(board_game, new_board_stat, depth - 1, alpha, beta, True, child))
                beta = min(beta, value)
                board_game[child[0]][child[1]] = '-'
                if beta <= alpha:
                    break
            return val

    def isTerminal(self, board_stat):
        for i in xrange(0, 9):
            if board_stat[i] == '-':
                return False
        return True

    def getUtilityVal(self, board_stat):
        for i in self.representative_three_matrix:
            myCount = 0
            otherCount = 0
            for j in i:
                if board_stat[j] == self.myMark:
                    myCount += 1
                elif board_stat[j] == self.other:
                    otherCount += 1
            if myCount == 3:
                return self.inf
            elif otherCount == 3:
                return -self.inf
        return 0

    def getHeuristicVal(self, board_game, board_stat):
        heuristic = 0
        for i in self.representative_three_matrix:
            myCount = 0
            otherCount = 0
            for j in i:
                if board_stat[j] == self.myMark:
                    myCount += 1
                elif board_stat[j] == self.other:
                    otherCount += 1
            heuristic += 100 * self.heuristic_value_matrix[myCount][otherCount]
        for i in xrange(0, 3):
            for j in xrange(0, 3):
                if board_stat[3 * i + j] != '-':
                    continue
                for representative_three_matrix in self.representative_three_matrix:
                    myCount = 0
                    otherCount = 0
                    for idx in representative_three_matrix:
                        r = 3 * i + idx/3
                        c = 3 * j + idx%3
                        if board_game[r][c] == self.myMark:
                            myCount += 1
                        elif board_game[r][c] == self.other:
                            otherCount += 1
                    heuristic += self.heuristic_value_matrix[myCount][otherCount]
        return heuristic

    def generateHeuristicMatrix(self):
        self.representative_three_matrix = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        self.heuristic_value_matrix = [[0, -10, -100, -1000], [10, 0, 0], [100, 0], [1000]]
