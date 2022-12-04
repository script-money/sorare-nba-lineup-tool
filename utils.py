import numpy as np


def ewma(x, alpha):
    """
    Returns the exponentially weighted moving average of x.

    Parameters:
    -----------
    x : array-like
    alpha : float {0 <= alpha <= 1}

    Returns:
    --------
    ewma: numpy array
          the exponentially weighted moving average
    """
    # Coerce x to an array
    x = np.array(x)
    n = x.size

    # Create an initial weight matrix of (1-alpha), and a matrix of powers
    # to raise the weights by
    w0 = np.ones(shape=(n, n)) * (1 - alpha)
    p = np.vstack([np.arange(i, i - n, -1) for i in range(n)])

    # Create the weight matrix
    w = np.tril(w0**p, 0)

    # Calculate the ewma
    return np.dot(w, x[:: np.newaxis]) / w.sum(axis=1)


def divide(a, b):
    if b == 0:
        return 0
    else:
        return round(a / b, 2)


def exclude_best_and_worst(stats_arr: list[float]) -> list[float]:
    """计算表现是去除最好最差的（除了最近一场）

    Args:
        stats_arr (list[float]): 统计

    Returns:
        list[float]: 过滤后的统计
    """
    worst = 0.0
    worst_index = 0
    best = 0.0
    best_index = 0
    other_games = stats_arr[1:]
    for index, game in enumerate(other_games):
        if game < worst:
            worst = game
            worst_index = index + 1
        if game > best:
            best = game
            best_index = index + 1
    return [k for i, k in enumerate(stats_arr) if i != worst_index and i != best_index]
