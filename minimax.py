

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

