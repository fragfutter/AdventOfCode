#!/usr/bin/python

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

INPUT = 'input_02.txt'

data = map(lambda x: x.strip(), open(INPUT, 'r').readlines())

pad = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 2, 3, 4, 0, 0],
    [0, 5, 6, 7, 8, 9, 0],
    [0, 0, 'A', 'B', 'C', 0, 0],
    [0, 0, 0, 'D', 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
pos = [3, 1]  # row, col

move = {
    'L': [0, -1],
    'R': [0, 1],
    'U': [-1, 0],
    'D': [1, 0],
}


def padval(coordinates):
    return pad[coordinates[0]][coordinates[1]]


for sequence in data:
    for step in sequence:
        newpos = list(map(sum, zip(pos, move[step])))
        if padval(newpos):
            pos = newpos
    logging.info('digit: %s', padval(pos))
