#!/usr/bin/python

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
import operator

INPUT = 'input_06.txt'

data = open(INPUT, 'r').readlines()

columns = [dict() for _ in range(8)]
for row in data:
    for (c, column) in zip(row, columns):
        try:
            column[c] += 1
        except KeyError:
            column[c] = 1

result = ''
for column in columns:
    result += max(column.items(), key=operator.itemgetter(1))[0]
logging.info(result)

# TWO
result = ''
for column in columns:
    result += min(column.items(), key=operator.itemgetter(1))[0]
logging.info(result)
