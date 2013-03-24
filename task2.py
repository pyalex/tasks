"""
    Log files Merge.

    Combines several log files into one with compliance with order
    Implementation is based on heap queue algorithm

"""
import os
import sys

import re
import datetime
import time
import heapq
import logging


# Use this constant for level filtration
LOGGING_LEVEL = logging.INFO


def str2timestamp(string):
    """ Convert DateTime string into UNIX timestamp """
    dt = datetime.datetime.strptime(string[:-6], '%a %b %d %Y %H:%M:%S')
    return int(time.mktime(dt.timetuple()))


def filter_level(level):
    """ Check log level using getLevelName
    which convert string ("error") into int (40) as well"""
    return logging.getLevelName(level.upper()) >= LOGGING_LEVEL


line_parts = [
    r'\[(?P<time>[^\]]+)\]',
    r'\[(?P<level>\w+)\]',
]
re_line = re.compile(' '.join(line_parts))


def file_iterator(file_obj, filename):
    """ Iterate over file object and discard undesirable lines by log level """

    lines = ((re_line.search(line).groups(), line.strip()) for line in file_obj
             if re_line.search(line))
    lines = ((str2timestamp(dt), (filename, line)) for (dt, level), line in lines
             if filter_level(level))
    return lines


def open_sources(filenames):
    """ Prepare all sources.
    Return dict {filename => iterator}
    """

    sources = {}
    for filename in filenames:
        if not os.path.isfile(filename):
            continue

        try:
            f = open(filename)
        except IOError:
            continue

        sources[filename] = file_iterator(f, filename)

    return sources


def read_line_from_file(queue, sources, filename):
    it = sources[filename]

    try:
        line = next(it)
    except StopIteration:
        del sources[filename]
        return

    heapq.heappush(queue, line)


def merge_log_files(filenames):
    """ Main function.
    1. Push one line from each file into heapq.
    2. Pop earliest line from heap root
    3. Recharge heapq with new line from the same file as popped
    """

    queue = []
    sources = open_sources(filenames)

    for filename in sources.keys():
        read_line_from_file(queue, sources, filename)

    while True:
        try:
            _, (filename, line) = heapq.heappop(queue)
        except IndexError:
            raise StopIteration

        if filename in sources:
            read_line_from_file(queue, sources, filename)

        yield line


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit('Usage python task2.py filename1 filename2 ...')

    result = merge_log_files(sys.argv[1:])

    while True:
        try:
            print next(result)
        except StopIteration:
            break