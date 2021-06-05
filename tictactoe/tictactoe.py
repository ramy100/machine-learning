"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    flat_board = [num for elem in board for num in elem]
    if flat_board.count(X) > flat_board.count(O):
        return O
    return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    res = set()
    for rowIndex, row in enumerate(board):
        available_moves_in_row = [(rowIndex,i) for i, x in enumerate(row) if x == None]
        for i in available_moves_in_row:
            res.add(i)
    return res


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row = action[0]
    col = action[1]
    board_copy = copy.deepcopy(board)
    turn = player(board)

    if board_copy[row][col] is not None:
        raise NameError('Invalid Move')

    board_copy[row][col] = turn
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    resH = ""
    resV = ""
    resD1 = f'{board[0][0]}{board[1][1]}{board[2][2]}'
    resD2 = f'{board[0][2]}{board[1][1]}{board[2][0]}'
    resD1 = resD1 if resD1 == "XXX" or resD1 == "OOO" else ""
    resD2 = resD2 if resD2 == "XXX" or resD2 == "OOO" else ""
    v_rotate_list = list(zip(*board[::-1]))

    for row in board:
        for col in row:
            resH += col or ""
        if resH == "OOO" or resH == "XXX":
            break
        resH = ""

    for row in v_rotate_list:
        for col in row:
            resV += col or ""
        if resV == "OOO" or resV == "XXX":
            break
        resV = ""
        
    winner = resD1 or resD2 or resH or resV
    if winner == "XXX":
        return X
    if winner == "OOO":
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    flat_board = [num for elem in board for num in elem]

    result = winner(board)
    tie = flat_board.count(EMPTY) == 0

    if result or tie:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        if winner(board) == X:
            return 1
        if winner(board) == O:
            return -1
        else:
            return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    best_action = None
    available_actions = actions(board)
    if player(board) == X:
        lowest_score = -math.inf
        for action in available_actions:
            current_score = min_value(result(board,action))

            if current_score > lowest_score:
                lowest_score = current_score
                best_action = action

    if player(board) == O:
        highest_score = math.inf
        for action in available_actions:
            current_score = max_value(result(board,action))

            if current_score < highest_score:
                highest_score = current_score
                best_action = action

    return best_action



def max_value(board):
    if terminal(board):
        return utility(board)
    v = -math.inf
    available_actions = actions(board)
    for action in available_actions:
        v = max(v , min_value(result(board,action)))
    return v

def min_value(board):
    if terminal(board):
        return utility(board)
    v = math.inf
    available_actions = actions(board)
    for action in available_actions:
        v = min(v , max_value(result(board,action)))
    return v
