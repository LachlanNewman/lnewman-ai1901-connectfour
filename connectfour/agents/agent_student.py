import time

from connectfour.agents.computer_player import RandomAgent
from connectfour.board import Board
import random


class StudentAgent(RandomAgent):
    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 1

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append(move)
            vals.append(self.dfMiniMax(next_state, 1))
        bestMove = moves[vals.index(max(vals))]
        return bestMove

    def dfMiniMax(self, board, depth):
        # Goal return column with maximized scores of all possible next states

        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])

            moves.append(move)
            vals.append(self.dfMiniMax(next_state, depth + 1))

        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal

    def evaluateBoardState(self, board: Board):
        """
        Your evaluation function should look at the current state and return a score for it. 
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """

        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.

        Board Variables:
            board.width 
            board.height
            board.last_move
            board.num_to_connect
            board.winning_zones
            board.score_array 
            board.current_player_score

        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """

        evaluation_value = 0
        for row,col in board.valid_moves():
            next_board = board.next_state(1,col)
            horizonatal_lines = self.get_horizontal_lines(next_board)
            vertical_lines = self.get_vertical_lines(next_board)
            diagonal_down_lines = self.get_diagonal_down_lines(next_board)
            diagonal_up_lines = self.get_diagonal_up_lines(next_board)
            lines = horizonatal_lines + vertical_lines + diagonal_down_lines + diagonal_up_lines
            evaluation_value += self.calc_line_weights(lines)

        # col = last_move[1]
        # col_val = 8
        # if col == 0 or col == 6:
        #     col_val = 0
        # if col == 1 or col == 5:
        #     col_val =  1
        # if col == 2 or col == 4:
        #     col_val = 2

        return  evaluation_value


    def calc_line_weights(self,lines):
        #for each line calc the number of times 2 appears
        player_2_cells = 0

        for line in lines:
            player_2_cells += self.player_2_cells(line)
        return player_2_cells


    def player_2_cells(self,line):
        p2_4_cells = 10000
        p2_empty_3_cells = 1000
        p2_empty_2_empty = 100
        p2_2_cells = 10
        p2_1_cells = 1

        p1_4_cells = -10000
        p1_empty_3_cells = -5000
        p1_empty_2_empty = -500
        p1_2_cells = -10
        p1_1_cells = -1

        count_player_1 = line.count(1)
        count_player_2 = line.count(2)
        count_empty = line.count(0)
        count = 0
        if count_player_2 == 4:
            count+= p2_4_cells
        if count_player_2 == 3 and count_empty == 1:
            count+= p2_empty_3_cells
        if count_player_2 == 2 and count_empty == 2:
            if line[0] == 0 and line[3]== 0:
                count+= p2_empty_2_empty
            else:
                count+= p2_2_cells
        if count_player_2 == 1 and count_empty == 3:
            count+= p2_1_cells
        if count_player_1 == 4:
            count+= p1_4_cells
        if count_player_1 == 3 and count_empty == 1:
                count += p1_empty_3_cells
        if count_player_1 == 2 and count_empty == 2:
            if line[0] == 0 and line[3]== 0:
                count += p1_empty_2_empty
            else:
                count += p1_2_cells
        if count_player_1 == 1 and count_empty == 3:
                count += p1_1_cells
        return count

    def player_1_cells(self,line):


        return 0

    def get_horizontal_lines(self,board):
        #starting with the move at 0
        lines = []
        for row in range(board.height - 1, 0, -1):
            for col in range(0,board.width - 3):
                line = []
                for val in range(col,col + 4):
                    try:
                        cell = board.get_cell_value(row,val)
                        line.append(cell)
                    except ValueError as e:
                        break
                lines.append(line)
        return lines

    def get_vertical_lines(self,board):
        lines = []
        for col in range(0,board.width):
            for row in range(board.height-1,board.height -4,-1):
                line = []
                for val in range(row,row - 4,-1):
                    try:
                        cell = board.get_cell_value(val,col)
                        line.append(cell)
                    except ValueError as e:
                        break
                lines.append(line)
        return lines

    def get_diagonal_up_lines(self,board):
        lines = []
        for col in range(0,board.width -1):
            for row in range(0, board.height):
                line = []
                for val in range(0,4):
                    try:
                        cell =  board.get_cell_value(row - val, col + val)
                        line.append(cell)
                    except ValueError as e:
                        break
                if len(line) == 4:
                    lines.append(line)
        return lines

    def get_diagonal_down_lines(self,board):
        lines = []
        for col in range(board.width -1,0,-1):
            for row in range(board.height-1,0,-1):
                line = []
                for val in range(0,4):
                    try:
                        cell =  board.get_cell_value(row + val, col - val)
                        line.append(cell)
                    except ValueError as e:
                        break
                if len(line) == 4:
                    lines.append(line)
        return lines

    # def check_threat(self,lines:list):
    #     for line in lines:
    #         count = 0
    #         for val in line:
    #             if val == 1:
    #                 count+=1
    #         if(count==3 and 0 in line):
    #             return True
    #     return False
    #
    # # player 1 move = odd number of free spots
    # # player 2 move = even number of free spots
    # # odd spot = spot belonging to and odd row
    # # even spot = spot belonging to and even row
    # # ODD THREAT = A threat whose empty spot is odd.
    # # EVEN  =  THREAT A threat whose empty spot is even.
    #
    # def check_row_below(self,board, last_move):
    #     last_move_row , last_move_col = last_move
    #     board_rows = board.board
    #     for board_row in board_rows:
    #         for cell in board_row:
    #             row = board_rows.index(board_row)
    #             col = board_row.index(cell)
    #             if cell == 1 and not self.surrouded(board,(row,col)):
    #
    #                 if row % 2 > 0:
    #     #                 playeer 1 played on odd row
    #     #                   play to left or right
    #                     if last_move_col == col + 1 or last_move_col == col - 1:
    #                         return 1
    #                     else: return 0
    #                 else:
    #                     if last_move_row == row + 1:
    #                         return 1
    #                     else:
    #                         return 0
    #     return 0
    #
    #
    # def surrouded(self, board, cell):
    #     row,col = cell
    #     is_surrounded = False
    #     try:
    #         is_surrounded = board.get_cell_value(row , col + 1 ) == 0
    #     except ValueError as e:
    #         print(e)
    #     try:
    #         is_surrounded = board.get_cell_value(row , col - 1) == 0
    #     except ValueError as e:
    #         print(e)
    #     return is_surrounded
