"""
    Sequence filtration:
        1. Drop heading empty strings
        2. Drop trailing empty strings
        3. Group repeating empty strings into one

    Usage:
        filter_seq(iterable)
        list(filter_seq(iterable)) if iterable is finite
        accept any iterable sequences
        -> returns generator
"""

import sys


def is_valid(value):
    """ Checking if string is empty """
    return bool(value.strip())


def filter_seq(iterable):
    """ Returns generator which yields filtered and grouped values"""

    input_iterator = iter(iterable)
    current_value = next(input_iterator)

    # Flag for dropping heading invalid strings
    drop_head = True

    while True:
        try:
            next_value = next(input_iterator)
        except StopIteration, exc:
            if is_valid(current_value):
                # don't forget to yield last value before exit
                yield current_value

            raise exc

        if is_valid(current_value) or (is_valid(next_value) and not drop_head):
            yield current_value
            drop_head = False

        current_value = next_value


def iterate_stdin():
    """ Generator for reading stdin in real-time"""

    while True:
        try:
            line = sys.stdin.readline()
        except KeyboardInterrupt:
            raise StopIteration

        if not line:
            raise StopIteration

        yield line.strip()


if __name__ == '__main__':
    result_iterator = filter_seq(iterate_stdin())

    while True:
        try:
            print next(result_iterator)
        except StopIteration:
            break
