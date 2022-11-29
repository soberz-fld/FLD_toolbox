def round_to_multiple_of_x(x: (int, float), n: (int, float)) -> (int, float):
    """
    Rounds n to a multiple of x
    :param x: Base value
    :param n: Number to round
    """
    t = type(x)
    modulo = n % x
    if modulo < x / 2:
        return t(n - modulo)
    else:
        return t(n + (x - modulo))
