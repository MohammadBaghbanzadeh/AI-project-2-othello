import copy
import math

def minimax(board, depth, alpha, beta, maximizer, active_player):
    if depth == 0 or board.end_game():
        return None, evaluate(board, active_player)

    children = board.successor(board)
    best_move = children[0]

    if maximizer:
        max_list = []
        max_eval = -math.inf
        for child in children:
            board_copy = copy.deepcopy(child)
            current_eval = minimax(board_copy, depth - 1, False, active_player)[1]
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
        return best_move, max_value

    else:
        min_list = []
        for child in children:
            board_copy = copy.deepcopy(child)
            current_eval = minimax(board_copy, depth - 1, True, active_player)[1]
            tup = (child, current_eval)
            min_list.append(tup)

        min_tuple = min(min_list, key=lambda p: p[1])
        best_move = min_tuple[0]
        min_value = min_tuple[1]
        return best_move, min_value

# w = max(players, key=lambda p: p.totalScore


def evaluate(board, player):
    white_utility = 0
    black_utility = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'b':
                black_utility += 1
            elif board[i][j] == 'w':
                white_utility += 1

    if player == 'b':
        utility = black_utility - white_utility
    else:
        utility = white_utility - black_utility

    return utility

