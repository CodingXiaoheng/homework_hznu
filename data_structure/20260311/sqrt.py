def sqrt(n):
    """
    Calculate the square root of a number.

    Returns:
    The square root of the input number. (float)

    Raises:
    TypeError: If the input is not a number.
    ValueError: If the input is negative.

    Examples:
    >>> sqrt(4)
    2.0
    >>> sqrt(9)
    3.0

    """
    if not isinstance(n, (int, float)):
        try:
            n = float(n)
        except ValueError:
            raise TypeError("Input must be a number")
    if n < 0:
        raise ValueError("Input cannot be negative")
    return n ** 0.5