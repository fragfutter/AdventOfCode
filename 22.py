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
sys.exit(0)

def move(grid, xa, ya, xb, yb):
    """move content from a to b"""
    # test if we can get the node b
    if xb < 0 or yb < 0:
        raise IndexError()
    try:
        a = grid[xa][ya]
        b = grid[xb][yb]
    except IndexError:
        raise
    # ok node exists, do they fit?
    if a[1] > (b[0] - b[1]):
        raise IndexError()
    # valid move, execute it
    result = copy.deepcopy(grid)
    result[xb][yb][1] += a[1]
    result[xb][yb][2] = a[2]
    result[xa][ya][1] = 0
    result[xa][ya][2] = False
    return result


def moves(steps, grid):
    steps += 1
    for x in range(X + 1):
        for y in range(Y + 1):
            for xb, yb in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                try:
                    result = move(grid, x, y, xb, yb)
                    # logging.debug('move (%d, %d) to (%d, %d)', x, y, xb, yb)
                    yield steps, result
                except IndexError:
                    pass

seen = []
bt = [(0, data)]
i = 0
while i < len(bt):
    steps, grid = bt[i]
    i += 1
    if grid[0][0][2]:
        logging.info('found it %d', steps)
        break
    if grid in seen:
        continue
    seen.append(grid)
    bt.extend(moves(steps, grid))
    logging.debug('i: %d, bt: %d', i, len(bt))
