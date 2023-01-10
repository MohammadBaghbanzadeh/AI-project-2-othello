import copy
import math
from Othello import Othello
from TranspositionTable import TranspositionTable
from print_board import print_matrix
import time
game = Othello()


def evaluate(board, player):
    all_pieces = [i for elem in board for i in elem]
    white_pieces = sum(1 for i in all_pieces if i == 'w')
    black_pieces = sum(1 for i in all_pieces if i == 'b')
    if white_pieces + black_pieces != len(all_pieces):
        return numDiffe(board, player) + count_corners(board, player) + \
               count_sides(board, player) + mobility(board, player)
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


# ____________________________________________________________
def mobility(board, player):
    global game
    black_mobility = len(game.successor(board, 'b'))
    white_mobility = len(game.successor(board, 'w'))
    if player == 'b' and (white_mobility + black_mobility) != 0:
        return 100 * (black_mobility / (white_mobility + black_mobility))
    elif player == 'w' and (white_mobility + black_mobility) != 0:
        return 100 * (white_mobility / (white_mobility + black_mobility))

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
    if not children:
        op = 'b' if active_player == 'w' else 'w'
        children = game.successor(board, op)
    if maximizer and children:
        max_list = []
        max_eval = -math.inf
        if type(children) != list:
            children = [children]
        for child in children:
            board_copy = copy.deepcopy(child)
            opponent0 = 'w' if active_player == 'b' else 'w'
            current_eval = alpha_beta(board_copy, depth - 1, alpha, beta, False, opponent0, current_level + 1, transposition_table)[1]
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
        res = best_move, max_value
        transposition_table.store(board, res, depth)
        return res

    elif not maximizer and children:
        min_list = []
        min_eval = math.inf
        for child in children:
            board_copy = copy.deepcopy(child)
            opponent1 = 'b' if active_player == 'w' else 'b'
            current_eval = alpha_beta(board_copy, depth - 1, alpha, beta, True, opponent1, current_level + 1, transposition_table)[1]
            tup = (child, current_eval)
            min_list.append(tup)
            if current_eval < min_eval:
                min_eval = current_eval
            beta = min(beta, current_eval)
            if beta <= alpha:
                break
        min_tuple = min(min_list, key=lambda p: p[1])
        best_move = min_tuple[0]
        min_value = min_tuple[1]
        res = best_move, min_value
        transposition_table.store(board, result, depth)
        return best_move, min_value
    else:
        return 0, 0

# ____________________________________________________________
def beam_search( board, player, depth, beam_width=2):

    if depth == 0:
        return [(evaluate(board, player), None)]  # Return the score of the current board state
    top_moves = []
    # Generate all possible states of the game
    for new_board in game.successor(board, player):
        opponent = 'b' if player == 'w' else 'w'
        # Recursively call beam_search for next level and next player
        score, _ = beam_search(new_board, opponent, depth-1, beam_width)[0]
        top_moves.append((score, new_board))
    top_moves.sort(reverse=True)  # sort by descending score
    return top_moves[:beam_width]

# ____________________________________________________________
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

    depth = 3
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
