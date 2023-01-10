import copy
import math
from Othello import Othello
from print_board import print_matrix
import time
game = Othello()


def evaluate(board, player):
    all_pieces = [i for elem in board for i in elem]
    white_pieces = sum(1 for i in all_pieces if i == 'w')
    black_pieces = sum(1 for i in all_pieces if i == 'b')
    if white_pieces + black_pieces != len(all_pieces):
        return numDiffe(board, player) + count_corners(board, player) + \
               count_sides(board, player) + mobility(board, player) \
               # + stability(board, player)
    else:
        return 0


# ____________________________________________________________

def numDiffe(board, turn):
    all_pieces = [i for elem in board for i in elem]
    white_pieces = sum(1 for i in all_pieces if i == 'w')
    black_pieces = sum(1 for i in all_pieces if i == 'b')

    if turn == 'b':
        return (black_pieces / (black_pieces + white_pieces)) * 100
    else:
        return (white_pieces / (black_pieces + white_pieces)) * 100
    # if white_pieces > black_pieces:
    #     return (white_pieces / (black_pieces + white_pieces)) * 100
    # else:
    #     return - (black_pieces / (black_pieces + white_pieces)) * 100


# ____________________________________________________________
def count_corners(board, player):
    # define the corners of the board
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
    # initialize the counts for each player
    white_count = 0
    black_count = 0

    # count the number of corners owned by each player
    for i, j in corners:
        if board[i][j] == "w":
            white_count += 1
        elif board[i][j] == "b":
            black_count += 1

    if player == 'b':
        return 25 * black_count
    elif player == 'w':
        return 25 * white_count
    else:
        return float(0)
    # return 25 * (white_count - black_count)


# ____________________________________________________________
def count_sides(board, player):
    white_count = 0
    black_count = 0

    # count the number of side pieces owned by each player
    for row in range(1, 7):
        if board[row][0] == 'b':
            black_count += 1
        elif board[row][0] == 'w':
            white_count += 1

        if board[row][7] == 'b':
            black_count += 1
        elif board[row][7] == 'w':
            white_count += 1

    for col in range(1, 7):
        if board[0][col] == 'b':
            black_count += 1
        elif board[0][col] == 'w':
            white_count += 1

        if board[7][col] == 'b':
            black_count += 1
        elif board[7][col] == 'w':
            white_count += 1

    if player == 'b':
        return 4 * black_count
    elif player == 'w':
        return 4 * white_count
    else:
        return float(0)
    # return 4 * (white_count - black_count)


# ____________________________________________________________
def mobility(board, player):
    global game
    black_mobility = len(game.successor(board, 'b'))
    white_mobility = len(game.successor(board, 'w'))
    # mobility = white_mobility / (white_mobility + black_mobility)
    # calculate Possibility
    # possibility = mobility * 100
    if player == 'b' and (white_mobility + black_mobility) != 0:
        return 100 * (black_mobility / (white_mobility + black_mobility))
    elif player == 'w' and (white_mobility + black_mobility) != 0:
        return 100 * (white_mobility / (white_mobility + black_mobility))
    # return possibility


# ____________________________________________________________
# def stability(board, player):
#     stability = [0, 0]
#     blackStability = stability[0]
#     whiteStability = stability[1]
#
#     opponent = 'b' if player == 'w' else 'w'
#
#     for i in range(8):
#         for j in range(8):
#             stable_pieces = 0
#             if board[i][j] == 0:
#                 continue
#
#             if (j == 0 or board[i][j - 1] == opponent) and (j == 7 or board[i][j + 1] == opponent):
#                 stable_pieces += 1
#
#             if (i == 0 or board[i - 1][j] == opponent) and (i == 7 or board[i + 1][j] == opponent):
#                 stable_pieces += 1
#
#             if (i == 0 or j == 0 or board[i - 1][j - 1] == opponent) and (
#                     i == 7 or j == 7 or board[i + 1][j + 1] == opponent):
#                 stable_pieces += 1
#
#             if (i == 0 or j == 7 or board[i - 1][j + 1] == opponent) and (
#                     i == 7 or j == 0 or board[i + 1][j - 1] == opponent):
#                 stable_pieces += 1
#
#             if stable_pieces >= 7:
#                 stability[board[i][j] - 1] -= 1
#
#             elif stable_pieces <= 3:
#                 stability[board[i][j] - 1] += 1
#
#     whiteStability = stability[1]
#     blackStability = stability[0]
#     if whiteStability + blackStability == 0:
#         return 0
#     else:
#         stability = whiteStability / (whiteStability + blackStability)
#         return 100 * stability


# ____________________________________________________________
def alpha_beta(board, depth, alpha, beta, maximizer, active_player, current_level=0):
    if depth == 0 or current_level == depth:
        return None, evaluate(board, active_player)

    global game
    children = game.successor(board, active_player)
    if not children:
        op = 'b' if active_player == 'w' else 'w'
        children = game.successor(board, op)
    if maximizer and children:
        # print(f"in maximizer children is: {'is empty' if not children else 'ful'}")
        # print(f"depth is: {depth}")
        max_list = []
        max_eval = -math.inf
        if type(children) != list:
            children = [children]
        for child in children:
            board_copy = copy.deepcopy(child)
            opponent0 = 'w' if active_player == 'b' else 'w'
            current_eval = alpha_beta(board_copy, depth - 1, alpha, beta, False, opponent0, current_level + 1)[1]
            tup = (child, current_eval)
            max_list.append(tup)
            if current_eval > max_eval:
                max_eval = current_eval
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break

        max_tuple = max(max_list, key=lambda p: p[1])
        best_move = max_tuple[0]
        max_value = max_tuple[1]
        return best_move, max_value

    elif not maximizer and children:
        # print(f"in minimizer children is: {children}")
        min_list = []
        for child in children:
            board_copy = copy.deepcopy(child)
            opponent1 = 'b' if active_player == 'w' else 'b'
            current_eval = alpha_beta(board_copy, depth - 1, alpha, beta, True, opponent1, current_level + 1)[1]
            tup = (child, current_eval)
            min_list.append(tup)
            if beta <= alpha:
                break
        min_tuple = min(min_list, key=lambda p: p[1])
        best_move = min_tuple[0]
        min_value = min_tuple[1]
        return best_move, min_value
    else:
        return 0, 0


if __name__ == "__main__":
    """
        AI TO AI MANAGER WITH ALPHA BETA PRUNING
    """
    player = 'b'
    arr = [['e' for i in range(8)] for j in range(8)]
    arr[3][3] = 'w'
    arr[4][4] = 'w'
    arr[4][3] = 'b'
    arr[3][4] = 'b'

    depth = 5
    print_matrix(arr)
    t = alpha_beta(arr, depth, -float('inf'), float('inf'), True, player, 0)
    print_matrix(t[0])
    print(t[1])
    arr = t[0]

    while not game.end_game(arr):
        opponent = 'b' if player == 'w' else 'w'
        if len(game.successor(arr, opponent)) != 0:
            player = 'b' if player == 'w' else 'w'
        print(f"-------------------{'white'if player=='w' else 'black'}-------------------")
        print_matrix(t[0], [], game.legal_moves(arr, player)[0])
        start = time.time()
        t = alpha_beta(arr, depth, -float('inf'), float('inf'), True, player, 0)
        print(time.time()-start)
        arr = t[0]
        winner, draw = 0, False
        if game.end_game(arr):
            all_coins = [item for i in arr for item in i]
            white_coins = sum(1 for i in all_coins if i == 'w')
            black_coins = sum(1 for i in all_coins if i == 'b')
            if black_coins != white_coins:
                winner = 'b' if black_coins > white_coins else 'w'
            else:
                draw = True
            print(f"-------------------{'white'if player=='w' else 'black'}-------------------")
            print_matrix(t[0], [], game.legal_moves(arr, player)[0])
            print("---------END GAME---------")
            if winner: print(
                f"Winner of the game is '{'Black player' if winner == 'b' else 'White player'}' and result "
                f"is: {max(white_coins, black_coins)} > {min(white_coins, black_coins)}")
            if draw: print(
                f"Game is Draw and result is: {max(white_coins, black_coins)} = {min(white_coins, black_coins)}")
