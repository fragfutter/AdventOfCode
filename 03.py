#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
import sys
import itertools

INPUT = 'input_03.txt'
TWO = len(sys.argv) > 1

data = open(INPUT, 'r').readlines()
data = [list(map(int, x.split())) for x in data]


def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n  # three times the same itertor
    return itertools.zip_longest(fillvalue=fillvalue, *args)


data2 = []
if TWO:
    for rows in grouper(3, data):
        data2.extend(map(sorted, zip(*rows)))
else:
    for row in data:
        data2.append(sorted(row))
data = data2

possibles = 0

for a, b, c in data:
    if a + b <= c:
        continue
    logging.debug('%s %s %s', a, b, c)
    possibles += 1

logging.info(possibles)
