import unittest
import itertools
import logging
from mock import patch

import task1
import task2


class FilterTest(unittest.TestCase):
    def test_empty_list(self):
        res = task1.filter_seq([])
        self.assertEqual(list(res), [])

    def test_list_with_strings(self):
        lst = ['aaa', 'bbb', 'ccc']
        res = task1.filter_seq(lst)
        self.assertEqual(list(res), lst)

    def test_list_with_starting_blank_strings(self):
        lst = ['', '', '', 'valid', 'string']
        res = task1.filter_seq(lst)
        self.assertEqual(list(res), lst[3:])

    def test_list_with_ending_blank_strings(self):
        lst = ['valid', 'string', '', '']
        res = task1.filter_seq(lst)
        self.assertEqual(list(res), lst[:2])

    def test_grouping_blank_strings(self):
        lst = ['a', '', '', 'b', '', 'c', '', '', 'd']
        res = task1.filter_seq(lst)
        self.assertEqual(list(res), ['a'] + lst[2:7]+ ['d'])

    def test_generator_filtering(self):
        lst = ['', 'a', '', '', 'b', '']
        gen = (x for x in lst)
        res = task1.filter_seq(gen)
        self.assertEqual(list(res), ['a', '', 'b'])

    def test_infinite_generator(self):
        gen = itertools.cycle(['', 'a', '', '', 'b', ''])
        res = task1.filter_seq(gen)
        self.assertEqual(list(itertools.islice(res, 5)), ['a', '', 'b', '', 'a'])


LOG_FILES = [
    [
        '[Wed Oct 24 2012 8:32:52 +0200] [error] [client 127.0.0.1] log1',
        '[Wed Oct 24 2012 11:32:52 +0200] [error] [client 127.0.0.1] log4'
    ],
    [
        '[Wed Oct 24 2012 9:32:52 +0200] [error] [client 127.0.0.1] log2',
        '[Wed Oct 24 2012 12:32:52 +0200] [info] [client 127.0.0.1] log5',
        '[Wed Oct 24 2012 14:32:52 +0200] [warning] [client 127.0.0.1] log7'
    ],
    [
        '[Wed Oct 24 2012 10:32:52 +0200] [error] [client 127.0.0.1] log3',
        '[Wed Oct 24 2012 13:32:52 +0200] [error] [client 127.0.0.1] log6'
    ],
]

SOURCES = {
    'a': task2.file_iterator(LOG_FILES[0], 'a'),
    'b': task2.file_iterator(LOG_FILES[1], 'b'),
    'c': task2.file_iterator(LOG_FILES[2], 'c')
}


class MergeFilesTest(unittest.TestCase):
    @patch('task2.open_sources', return_value=SOURCES)
    def test_merge(self, isfile):
        task2.LOGGING_LEVEL = logging.DEBUG

        res = task2.merge_log_files(['a', 'b', 'c'])

        logs = [line[-1] for line in res]
        self.assertEqual(logs, map(str, range(1, 8)))

    def test_level_filtration(self):
        task2.LOGGING_LEVEL = logging.WARNING

        lines = task2.file_iterator(LOG_FILES[1], 'a')
        self.assertEqual(len(list(lines)), 2)

        task2.LOGGING_LEVEL = logging.ERROR

        lines = task2.file_iterator(LOG_FILES[1], 'a')
        self.assertEqual(len(list(lines)), 1)


if __name__ == '__main__':
    unittest.main()