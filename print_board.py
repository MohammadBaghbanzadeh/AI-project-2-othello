class Character:
    empty = '.'
    white = '■'
    black = '□'
    next = 'o'
    alphabet_label = "    A  B  C  D  E  F  G  H"
    numerical_label = "    0  1  2  3  4  5  6  7"
    line = 24 * '-'


class Colors:
    reset = '\033[0m'
    BOLD = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
    FAIL = '\033[91m'
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    blue = '\033[34m'
    purple = '\033[35m'
    cyan = '\033[36m'
    lightgrey = '\033[37m'
    darkgrey = '\033[90m'
    OKGREEN = '\033[92m'
    yellow = '\033[93m'
    lightblue = '\033[94m'
    pink = '\033[95m'
    lightcyan = '\033[96m'
    white = '\033[97m'

    class BG:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


"""
    print_matrix:
        argument -> 2D matrix with characters 'e', 'b' or 'w'
        return -> nothing
"""


def print_matrix(board, empty_surrounding=[], possible_moves=[]):
    row = len(board)
    col = len(board[0])

    for i in range(row):
        for j in range(col):
            # printing header of the board
            if i == 0 and j == 0:
                print(Colors().yellow + Colors().BOLD + Character.numerical_label + Colors().reset)
                print(Colors().FAIL + '   ' + Character.line + Colors().reset)
            if j == 0:
                print(Colors().OKGREEN + str(i) + Colors().FAIL + " | " + Colors().reset, end='')
            # printing the othello board
            if j != col - 1:
                if board[i][j].lower() == 'b':
                    print(Character.black, end="  ")
                elif board[i][j].lower() == 'w':
                    print(Character.white, end="  ")
                else:
                    if (i, j) in possible_moves:
                        print(Colors().orange + Character.next + Colors().reset, end="  ")
                    else:
                        print(Character.empty, end="  ")
            else:
                if board[i][j].lower() == 'b':
                    print(Character.black, end="  ")
                elif board[i][j].lower() == 'w':
                    print(Character.white, end="  ")
                else:
                    if (i, j) in possible_moves:
                        print(Colors().orange + Character.next + Colors().reset, end="  ")
                    else:
                        print(Character.empty, end="  ")
            # printing footer of the board
            if j == col - 1:
                print(Colors().FAIL + " | " + Colors().reset, end='')
            if i == row - 1 and j == col - 1:
                print()
                print(Colors().FAIL + '   ' + Character.line + Colors().reset)
                print(Colors().yellow + Colors().BOLD + Character.alphabet_label + Colors().reset)
        print()
