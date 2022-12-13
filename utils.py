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


def rename_player(
    name,
):
    match name:
        case "David Duke":
            return "David Duke Jr."
        case "Nicolas Claxton":
            return "Nic Claxton"
        case "Cameron Thomas":
            return "Cam Thomas"
        case "Jeff Dowtin":
            return "Jeff Dowtin Jr."
        case "Ishmail Wainright":
            return "Ish Wainright"
        case "Dario Saric":
            return "Dario Šarić"
        case "John Butler":
            return "John Butler Jr."
        case "Greg Brown":
            return "Greg Brown III"
        case "Jusuf Nurkic":
            return "Jusuf Nurkić"
        case "Bojan Bogdanovic":
            return "Bojan Bogdanović"
        case "Moe Wagner":
            return "Moritz Wagner"
        case "Brandon Boston Jr.":
            return "Brandon Boston"
        case "Marcus Morris":
            return "Marcus Morris Sr."
        case "Davis Bertans":
            return "Davis Bertāns"
        case "Luka Doncic":
            return "Luka Dončić"
        case "Jabari Smith":
            return "Jabari Smith Jr."
        case "Boban Marjanovic":
            return "Boban Marjanović"
        case "Kevin Porter":
            return "Kevin Porter Jr."
        case "Trevor  Hudgins":
            return "Trevor Hudgins"
        case "Dennis Schroder":
            return "Dennis Schröder"
        case "Nah'Shon Hyland":
            return "Bones Hyland"
        case "Nikola Jokic":
            return "Nikola Jokić"
        case "Vlatko Cancar":
            return "Vlatko Čančar"
        case "Nikola Vucevic":
            return "Nikola Vučević"
        case "Goran Dragic":
            return "Goran Dragić"
        case "Marko Simonovic":
            return "Marko Simonović"
        case "Dom Barlow":
            return "Dominick Barlow"
        case "Nikola Jovic":
            return "Nikola Jović"
        case "R.J. Barrett":
            return "RJ Barrett"
        case "Bogdan Bogdanovic":
            return "Bogdan Bogdanović"
        case "AJ Green":
            return "A.J. Green"
        case _:
            return name
