from math import floor


def time_as_string(t: int) -> str:
    """
    Returns the time as a string. (ex. 2 turns into "just now" and 121 turns
    into "2 minutes ago")

    :param t: The time, as an integer.
    :return: A string.
    """
    if t < 10:
        return "just now"
    elif t < 60:
        t = t - t % 10
        return f"{t} seconds ago"
    elif t < 60 * 60:
        t = floor(t / 60)
        return f"{t} minute{'' if t == 1 else 's'} ago"
    else:
        return "a long time ago"
