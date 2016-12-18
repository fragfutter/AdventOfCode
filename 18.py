#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

SIZE = 400000
data = open('input_18.txt', 'r').read().strip()
# data = '.^^.^.^^^^'
LEN = len(data)

TRAPS = [
    [True, True, False],
    [False, True, True],
    [True, False, False],
    [False, False, True],
]


def parse_row(data):
    result = list(map(lambda x: x == '^', data))
    return result


def is_trap(row, col):
    if col == 0:
        pattern = grid[row - 1][0:2]
        pattern.insert(0, False)
    elif col == LEN - 1:
        pattern = grid[row - 1][-2:]
        pattern.append(False)
    else:
        pattern = grid[row - 1][col - 1: col + 2]
    return pattern in TRAPS


def dump(grid):
    for row in grid:
        print(''.join(['^' if x else '.' for x in row]))


grid = [parse_row(data), ]
for i in range(1, SIZE):
    new_row = list(map(lambda x: is_trap(i, x), range(LEN)))
    grid.append(new_row)

total = sum(map(len, grid))
traps = sum(map(sum, grid))
logging.info('total %d, traps %d, safe %d', total, traps, total - traps)
