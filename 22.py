#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
import collections
import itertools
import re
import copy

pattern = re.compile('.*x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%')
Node = collections.namedtuple(
    'Node',
    ('x', 'y', 'size', 'used', 'avail', 'percent'),
)


def parse_line(line):
    data = list(map(int, pattern.match(line).groups()))
    result = Node(*data)
    return result


data = list(map(parse_line, open('input_22.txt', 'r').readlines()[2:]))


def pairs(data):
    result = []
    for a, b in itertools.permutations(data, 2):
        if a.used == 0:
            continue
        if a.used <= b.avail:
            result.append((a, b))
    return result

logging.info('part 1: %d', len(pairs(data)))


X = max(map(lambda x: x.x, data))
Y = max(map(lambda y: y.y, data))
SMALL = min(map(lambda s: s.size, data))
logging.debug('X: %d, Y: %d', X, Y)


def to_grid(data):
    result = [[0, 0, False], ] * (Y + 1)
    result = [copy.deepcopy(result) for x in range(X + 1)]
    for node in data:
        result[node.x][node.y] = [node.size, node.used, False]
    result[X][0][2] = True
    return result

data = to_grid(data)


def print_grid(grid):
    for x in range(X + 1):
        for y in range(Y + 1):
            n = grid[x][y]
            if n[2]:
                print('G', end='')
            elif n[1] == 0:
                print('_', end='')
            elif x == y == 0:
                print('x', end='')
            elif n[1] > SMALL:
                print('#', end='')
            else:
                print('.', end='')
        print('')

print_grid(data)
# solve it by hand.
# moving the empty space above G => n steps
# moving both G and empty one space up => 5 steps
# for the last move only move the G
# total => n + (X - 1)*5 + 1
