def maximize(board, k):
    if game_end(board):
        return None, 500
    if k == 0:
        return None, 500
    k -= 1
    (max_child, max_utility) = (None, -math.inf)
    for move in generatepossbilemoves(board):
        (temp, utility) = minimize(move, k)
        minimax_tree.append((utility, k))
        if utility > max_utility:
            (max_child, max_utility) = (move, utility)
    return max_child, max_utility


def minimize(board, k):
    if game_end(board):
        return (None, -500)
    if k == 0:
        return None, 500
    k -= 1
    (min_child, min_utility) = (None, math.inf)
    for move in generatepossbilemoves(board):
        temp, utility = maximize(move, k)
        minimax_tree.append((utility, k))
        if utility < min_utility:
            (min_child, min_utility) = (move, utility)
    return min_child, min_utility


def decision(board):
    child, utility = maximize(board, k)
    return child


def maximize_pruning(board, alpha, beta, k):
    if game_end(board):
        return None, 500
    if k == 0:
        return None, 500
    k -= 1
    (max_child, max_utility) = (None, -math.inf)
    for move in generatepossbilemoves(board):
        (temp, utility) = minimize_pruning(move, alpha, beta, k)
        if utility > max_utility:
            (max_child, max_utility) = (move, utility)
        if max_utility > alpha:
            max_utility = alpha
        if max_utility > beta:
            break
    return max_child, max_utility


def minimize_pruning(board, alpha, beta, k):
    if game_end(board):
        return (None, -500)
    if k == 0:
        return None, 500
    k -= 1
    (min_child, min_utility) = (None, math.inf)
    for move in generatepossbilemoves(board):
        temp, utility = maximize_pruning(move, alpha, beta, k)
        if utility < min_utility:
            (min_child, min_utility) = (move, utility)
        if min_utility < alpha:
            break
        if min_utility < beta:
            beta = min_utility
    return min_child, min_utility


def decision_pruning(board):
    child, utility = maximize_pruning(board, -math.inf, math.inf, k)
    return child