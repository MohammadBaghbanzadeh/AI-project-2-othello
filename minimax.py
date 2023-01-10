import copy
import math
from Othello import Othello
from TranspositionTable import TranspositionTable
from print_board import print_matrix
game = Othello()


def evaluate(board, player):
    return numDiffe(board, player) + count_corners(board, player) + \
           count_sides(board, player) + mobility(board, player) \
           # + stability(board, player)


# ____________________________________________________________

def numDiffe(board, player):
    all_pieces = [i for elem in board for i in elem]
    white_pieces = sum(1 for i in all_pieces if i == 'w')
    black_pieces = sum(1 for i in all_pieces if i == 'b')

    if player == 'b':
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
    else:
        return 25 * white_count

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
    else:
        return 4 * white_count
    # return 4 * (white_count - black_count)


# ____________________________________________________________
def mobility(board, player):
    global game
    black_mobility = len(game.successor(board, 'b'))
    white_mobility = len(game.successor(board, 'w'))
    # mobility = white_mobility / (white_mobility + black_mobility)
    # calculate Possibility
    # possibility = mobility * 100
    if player == 'b':
        return 100 * (black_mobility / (white_mobility + black_mobility))
    else:
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
def alpha_beta(board, depth, alpha, beta, maximizer, active_player, current_level=0, transposition_table=TranspositionTable()):
    result = transposition_table.retrieve(board, depth)
    if result:
        return result
    
    if depth == 0 or current_level == depth:
        result = None, evaluate(board, active_player)
        transposition_table.store(board, result, depth)
        return result
    

    global game
    children = game.successor(board, active_player)
    best_move = children[0]

    if maximizer:
        max_list = []
        max_eval = -math.inf
        for child in children:
            board_copy = copy.deepcopy(child)
            current_eval = alpha_beta(board_copy, depth - 1, alpha, beta, False, active_player, current_level + 1,transposition_table)[1]
            tup = (child, current_eval)
            max_list.append(tup)
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = child
            alpha = max(alpha, current_eval)
            if beta <= alpha:
                break

        max_tuple = max(max_list, key=lambda p: p[1])
        best_move = max_tuple[0]
        max_value = max_tuple[1]
        result = best_move, max_value
        transposition_table.store(board, result, depth)
        return result

    else:
        min_list = []
        for child in children:
            board_copy = copy.deepcopy(child)
            current_eval = alpha_beta(board_copy, depth - 1, alpha, beta, True, active_player, current_level + 1,transposition_table)[1]
            tup = (child, current_eval)
            min_list.append(tup)

        min_tuple = min(min_list, key=lambda p: p[1])
        best_move = min_tuple[0]
        min_value = min_tuple[1]
        result = best_move, min_value
        transposition_table.store(board, result, depth)
        return result

if __name__ == "__main__":
    arr = [
        ['w', 'b', 'w', 'w', 'w', 'e', 'e', 'e'],
        ['e', 'b', 'e', 'w', 'e', 'b', 'e', 'e'],
        ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
        ['e', 'b', 'e', 'b', 'b', 'e', 'e', 'e'],
        ['e', 'b', 'e', 'b', 'b', 'b', 'e', 'e'],
        ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
        ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
        ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e']
    ]
    print_matrix(arr)
    t = alpha_beta(arr, 2, -float('inf'), float('inf'), True, 'b', 0)
    print_matrix(t[0])
    print(t[1])

