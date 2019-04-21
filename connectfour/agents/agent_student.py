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
        print('------------')
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
        # score_array = board.score_array
        # last_move = board.last_move
        # if(self.check_threats(board,last_move)):
        #     return 1
        #
        # # check vertical count
        # vertical_count = 0

        #
        horizonatal_lines = self.get_horizontal_lines(board)
        vertical_lines  = self.get_vertical_lines(board)
        diagonal_up_lines = self.get_diagonal_up_lines(board)
        diagonal_down_lines = self.get_diagonal_down_lines(board)
        if(self.check_threat(horizonatal_lines) or self.check_threat(vertical_lines)
            or self.check_threat(diagonal_up_lines) or self.check_threat(diagonal_down_lines)):
            return 0

        return self.calc_line_weights(horizonatal_lines+vertical_lines+diagonal_down_lines+diagonal_up_lines)


    def calc_line_weights(self,lines):
        #for each line calc the number of times 2 appears
        player_2_cells = 0
        player_1_cells = 0

        number_of_elements = len(lines) * 1000.0
        for line in lines:
            for cell in line:
                count_player_2 = line.count(2)
                player_2_cells += self.player_2_cells(line)
                player_1_cells += self.player_1_cells(line)
        return (player_2_cells - player_1_cells) / number_of_elements


    def player_2_cells(self,line):
        four_cells = 1000
        three_cells = 100
        two_cells = 10
        one_cells = 1

        count_player_2 = line.count(2)
        if count_player_2 == 4:
            return four_cells
        if count_player_2 == 3:
            return three_cells
        if count_player_2 == 2:
            return two_cells
        if count_player_2 == 1:
            return one_cells
        return 0

    def player_1_cells(self,line):
        two_cells = 10
        one_cells = 1

        count_player_1 = line.count(2)
        if count_player_1 == 2:
            return two_cells
        if count_player_1 == 1:
            return one_cells
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

    def check_threat(self,lines:list):
        for line in lines:
            count = 0
            for val in line:
                if val == 1:
                    count+=1
            if(count==3 and 0 in line):
                return True
        return False
    # def evaluate_move(self,board,move):
    #     row,col = move
    #
    #     #check_vertical
    #     count = 0
    #     directions = 7.0
    #     num_pieces_needed = 3.0
    #
    #     for piece in range(1,board.num_to_connect):
    #         try:
    #             if piece == 0:
    #                 continue
    #             if board.get_cell_value(row + piece,col) == 2:
    #                 count+= 1
    #         except ValueError as e:
    #             continue
    #
    #     #  check horizontal
    #     for piece in range(-3,board.num_to_connect):
    #         try:
    #             if piece == 0:
    #                 continue
    #             if board.get_cell_value(row,col - piece) == 2:
    #                 count+= 1
    #         except ValueError as e:
    #             continue
    #
    #     #check diagonal
    #     for piece in range(-3,board.num_to_connect):
    #         try:
    #             if piece == 0:
    #                 continue
    #             if board.get_cell_value(row - piece ,col - piece) == 2:
    #                 count+= 1
    #         except ValueError as e:
    #             continue
    #
    #     for piece in range(-3,board.num_to_connect):
    #         try:
    #             if piece == 0:
    #                 continue
    #             if board.get_cell_value(row + piece,col + piece) == 2:
    #                 count+= 1
    #         except ValueError as e:
    #             continue
    #
    #     return count/ (directions * num_pieces_needed)


    # def check_threats(self,board,move):
    #     row,col = move
    #
    #     #check_vertical
    #     count = 0
    #     for piece in range(1,board.num_to_connect):
    #         try:
    #             if piece == 0:
    #                 continue
    #             if board.get_cell_value(row + piece,col) == 1:
    #                 count+= 1
    #             if board.get_cell_value(row + piece, col) == 2:
    #                 count-= 1
    #         except ValueError as e:
    #             break
    #
    #     if(count >= 3):
    #         return True
    #
    #     count = 0
    #     for piece in range(-3,board.num_to_connect):
    #         try:
    #             if piece == 0:
    #                 continue
    #             if board.get_cell_value(row,col + piece) == 1:
    #                 count+= 1
    #             if board.get_cell_value(row, col + piece) == 2:
    #                 count-= 1
    #         except ValueError as e:
    #             break
    #
    #     if(count >= 3):
    #         return True
    #
    #     count = 0
    #     for piece in range(-3,board.num_to_connect):
    #         try:
    #             if piece == 0:
    #                 continue
    #             if board.get_cell_value(row + piece ,col + piece) == 1:
    #                 count+= 1
    #             if board.get_cell_value(row + piece, col + piece) == 2:
    #                 count-= 1
    #         except ValueError as e:
    #             break
    #
    #     if(count == 3):
    #         return True
    #
    #     count = 0
    #     for piece in range(-3,board.num_to_connect):
    #         try:
    #             if piece == 0:
    #                 continue
    #             if board.get_cell_value(row + piece,col - piece) == 1:
    #                 count+= 1
    #             if board.get_cell_value(row + piece, col - piece) == 2:
    #                 count-= 1
    #         except ValueError as e:
    #             break
    #
    #     if(count == 3):
    #         return True
    #
    #     return False

    # def evaluate_vertical(self, board, cell):
    #      player1_score = 0
        # player2_score = 0
        # row,col = cell
        # directions = 8.0
        # number_connects_needed = board.num_to_connect - 1
        # for r in range(1,3):
        #     try:
        #         cell_value = board.get_cell_value(row + r, col)
        #         if cell_value == self.id:
        #             count += 1
        #         elif cell_value == 0:
        #             count + 0
        #         else:
        #             count-= 1
        #     except ValueError as e:
        #         continue
        #
        # for r in range(1,3):
        #     try:
        #         cell_value = board.get_cell_value(row - r, col)
        #         if cell_value == self.id:
        #             count += 1
        #         elif cell_value == 0:
        #             count + 0
        #         else:
        #             count-= 1
        #     except ValueError as e:
        #         continue
        #
        # for c in range(1, 3):
        #     try:
        #         cell_value = board.get_cell_value(row, col + c)
        #         if cell_value == self.id:
        #             count += 1
        #         elif cell_value == 0:
        #             count + 0
        #         else:
        #             count-= 1
        #     except ValueError as e:
        #         continue
        #
        # for c in range(1, 3):
        #     try:
        #         cell_value = board.get_cell_value(row, col - c)
        #         if cell_value == self.id:
        #             count += 1
        #         elif cell_value == 0:
        #             count + 0
        #         else:
        #             count-= 1
        #     except ValueError as e:
        #         continue
        #
        # for d in range(1, 3):
        #     try:
        #         cell_value = board.get_cell_value(cell[0] + d, cell[1] + d)
        #         if cell_value == self.id:
        #             count += 1
        #         elif cell_value == 0:
        #             count + 0
        #         else:
        #             count - 1
        #     except ValueError as e:
        #         continue
        #
        # for d in range(1, 3):
        #     try:
        #         cell_value = board.get_cell_value(cell[0] - d, cell[1] - d)
        #         if cell_value == self.id:
        #             count + 1
        #         elif cell_value == 0:
        #             count + 0
        #         else:
        #             count-= 1
        #     except ValueError as e:
        #         continue
        #
        # for d in range(1, 3):
        #     try:
        #         cell_value = board.get_cell_value(cell[0] + d, cell[1] - d)
        #         if cell_value == self.id:
        #             count + 1
        #         elif cell_value == 0:
        #             count + 0
        #         else:
        #             count-= 1
        #     except ValueError as e:
        #         continue
        #
        # for d in range(1, 3):
        #     try:
        #         cell_value = board.get_cell_value(cell[0] - d, cell[1] + d)
        #         if cell_value == self.id:
        #             count + 1
        #         elif cell_value == 0:
        #             count + 0
        #         else:
        #             count-= 1
        #     except ValueError as e:
        #         continue
        # x = count / (directions * number_connects_needed)
        # return x
