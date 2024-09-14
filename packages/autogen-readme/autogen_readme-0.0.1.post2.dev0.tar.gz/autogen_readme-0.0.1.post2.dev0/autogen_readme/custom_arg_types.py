import argparse

MIN_VAL = 0
MAX_VAL = 1


def float_type_between_0_and_1(arg):
    """Type function for argparse - a float within some predefined bounds"""
    try:
        f = float(arg)
    except ValueError:
        raise argparse.ArgumentTypeError("Must be a floating point number")
    if f < MIN_VAL or f > MAX_VAL:
        raise argparse.ArgumentTypeError(
            "Argument must be < " + str(MAX_VAL) + "and > " + str(MIN_VAL)
        )
    return f
    return f
