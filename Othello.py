from copy import deepcopy
from print_board import print_matrix
from ai import AI


def in_board(_i, _j, r, c):
    return (0 <= _i <= r - 1) and (0 <= _j <= c - 1)

class Othello:

    def __init__(self, useAI=False):
        self.board = []
        self.useAI = useAI
        self.ai_engine = AI()

    def legal_moves(self, board, _player):
        empty_surrounding_cells = self.find_empty(board)
        next_moves, pair_moves = self.find_correct_moves(board, empty_surrounding_cells, _player)
        next_moves = list(set(next_moves))
        next_moves.sort(key=lambda x: x[0])
        return next_moves, empty_surrounding_cells, pair_moves

    def end_game(self, board):
        all_pieces = [i for elem in board for i in elem]
        no_white_pieces = sum(1 for i in all_pieces if i == 'w')
        no_black_pieces = sum(1 for i in all_pieces if i == 'b')
        no_empty_cells = sum(1 for i in all_pieces if i == 'e')

        # There is no empty cell to doing a valid move:
        if no_empty_cells == 0 and no_white_pieces + no_black_pieces == len(all_pieces):
            return True

        # There is some empty cell but there is no any valid moves any more:
        white_valid_moves = self.find_correct_moves(board, self.find_empty(board), 'w')[0]
        black_valid_moves = self.find_correct_moves(board, self.find_empty(board), 'b')[0]
        if white_valid_moves == [] and black_valid_moves == []:
            return True

        return False

    def p2p_manager(self):
        player = 'b'
        arr = [['e' for i in range(8)] for j in range(8)]
        arr[3][3] = 'w'
        arr[4][4] = 'w'
        arr[4][3] = 'b'
        arr[3][4] = 'b'

        while not self.end_game(arr):
            if len(self.legal_moves(arr, player)[0]) == 0:
                print(f"{'white' if player == 'w' else 'black'} has no legal move, so changed the turn.")
                player = 'w' if player == 'b' else 'b'
            print_matrix(arr, [], self.legal_moves(arr, player)[0])
            try:
                ind = tuple(map(int, input(f"it's {'white' if player == 'w' else 'black'} turn:\t").split(" ")))
            except ValueError:
                print(f"ValueError: INDEX OF CELLS MUST BE LIKE, X Y")
                exit()

            print('------------------------------')
            while ind not in self.legal_moves(arr, player)[0]:
                print("\tYou Entered Illegal Move!")
                print("\tTry again, ", end='')
                ind = tuple(map(int, input(f"it's {'white' if player == 'w' else 'black'} turn:\t").split(" ")))

            pair_of_move = self.legal_moves(arr, player)[2]
            arr = self.change_between(arr, ind, pair_of_move[ind], player)

            # Check if the opponent has a valid move, then switch the turn.
            opponent = 'b' if player == 'w' else 'w'
            if self.find_correct_moves(arr, self.find_empty(arr), opponent)[0]:
                player = 'b' if player == 'w' else 'w'

            winner, draw = 0, False
            if self.end_game(arr):
                all_coins = [item for i in arr for item in i]
                white_coins = sum(1 for i in all_coins if i == 'w')
                black_coins = sum(1 for i in all_coins if i == 'b')
                if black_coins != white_coins:
                    winner = 'b' if black_coins > white_coins else 'w'
                else:
                    draw = True
                print("---------END GAME---------")
                if winner: print(
                    f"Winner of the game is '{'Black player' if winner == 'b' else 'White player'}' and result "
                    f"is: {max(white_coins, black_coins)} > {min(white_coins, black_coins)}")
                if draw: print(
                    f"Game is Draw and result is: {max(white_coins, black_coins)} = {min(white_coins, black_coins)}")

    @staticmethod
    def find_empty(board):
        row = len(board)
        col = len(board[0])
        empties = []

        for i in range(row):
            for j in range(col):
                if board[i][j] == 'e':
                    continue
                else:
                    #              left_up, right_down, right_up, left_down, down, up, left, right
                    directions = [(-1, -1), (1, 1), (-1, 1), (1, -1), (-1, 0), (1, 0), (0, -1), (0, 1)]
                    for Dir in directions:
                        _i, _j = Dir[0], Dir[1]
                        if in_board(i + _i, j + _j, row, col):
                            if board[i + _i][j + _j] == 'e':
                                empties.append((i + _i, j + _j))

        return list(set(empties))

    @staticmethod
    def find_correct_moves(board, empty_cells, player):
        def add_key(dictionary, key, value):
            try:
                dictionary[key]
            except KeyError:
                temp = {}
                temp[key] = value
                dictionary.update(temp)
                return dictionary
            if dictionary != {}:
                old_value = dictionary[key]
                new_value = []
                if type(old_value) == list:
                    old_value: 'list'
                    new_value = old_value.append(value)
                else:
                    old_value: 'tuple'
                    new_value.append(old_value)
                    new_value.append(value)
                    dictionary[key] = new_value
                return dictionary
            else:
                temp = {}
                temp[key] = value
                dictionary.update(temp)
                return dictionary

        #              left_up, right_down, right_up, left_down, down, up, left, right
        directions = [(-1, -1), (1, 1), (-1, 1), (1, -1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        row, col = len(board), len(board[0])
        correct_moves = []
        pair_correct_moves = {}
        opponent = 'b' if player == 'w' else 'w'

        for index in empty_cells:
            i = index[0]
            j = index[1]

            for Dir in directions:
                _i = Dir[0]
                _j = Dir[1]
                if 0 <= i + _i <= row - 1 and 0 <= j + _j <= col - 1:
                    if board[i + _i][j + _j] == opponent and in_board(i, j, row, col):
                        ii, jj = i + 2 * _i, j + 2 * _j

                        while in_board(ii, jj, row, col):
                            if board[ii][jj] == opponent:
                                ii += _i
                                jj += _j
                            elif board[ii][jj] != 'e':
                                correct_moves.append((i, j))
                                pair_correct_moves = add_key(pair_correct_moves, (i, j), (ii, jj))
                                break
                            else:
                                break

        return correct_moves, pair_correct_moves

    @staticmethod
    def change_between(board, move, pair_moves, turn):
        arr = []
        i = move[0]
        j = move[1]
        if type(pair_moves) == tuple:
            pair_moves = [pair_moves]

        for elem in pair_moves:
            if i == elem[0]:
                left_col = min(j, elem[1])
                right_col = max(j, elem[1])
                arr.extend([(i, j) for j in range(left_col + 1, right_col)])
            if j == elem[1]:
                down_row = max(i, elem[0])
                up_row = min(i, elem[0])
                arr.extend([(i, j) for i in range(up_row + 1, down_row)])
            # diagonal
            if abs(elem[0] - i) == abs(elem[1] - j):
                ii = i
                jj = j

                # up-right
                if elem[0] - i < 0 and elem[1] - j > 0:
                    for k in range(elem[1] - j - 1):
                        ii -= 1
                        jj += 1
                        arr.append((ii, jj))
                # up-left
                if elem[0] - i < 0 and elem[1] - j < 0:
                    for k in range(abs(elem[1] - j) - 1):
                        ii -= 1
                        jj -= 1
                        arr.append((ii, jj))
                # down-right
                if elem[0] - i > 0 and elem[1] - j > 0:
                    for k in range(elem[1] - j - 1):
                        ii += 1
                        jj += 1
                        arr.append((ii, jj))
                # down-left
                if elem[0] - i > 0 and elem[1] - j < 0:
                    for k in range(elem[0] - i - 1):
                        ii += 1
                        jj -= 1
                        arr.append((ii, jj))

        board[move[0]][move[1]] = turn
        for i in arr:
            board[i[0]][i[1]] = turn
        return board

    def successor(self, board, turn):
        result = self.legal_moves(board, turn)
        next_move, empties, pair_moves = result[0], result[1], result[2]
        successor_arr = []
        if type(next_move) != list:
            next_move = [next_move]
        for move in next_move:
            tmp = deepcopy(board)
            tmp = self.change_between(tmp, move, pair_moves[move], turn)
            successor_arr.append(tmp)
        # for mat in successor_arr:
        #     print_matrix(mat)
        return successor_arr

    def ai2ai_manager(self):
        # after completing the AI class this game manager will be manage game between two ai player.
        pass
