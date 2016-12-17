#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
import hashlib

START = 'veumntbg'


def md5(data):
    return hashlib.md5(data.encode('ascii')).hexdigest()


def doors(seed):
    digest = md5(seed)
    result = []
    for i, j in zip(digest[:4], 'UDLR'):
        if i in 'bcdef':
            result.append(j)
    return result


def walk(x, y, direction):
    w = {
        'U': (0, -1),
        'D': (0, 1),
        'L': (-1, 0),
        'R': (1, 0),
    }
    result = list(map(sum, zip((x, y), w[direction])))
    if -1 in result or 4 in result:
        raise IndexError()
    return result


pos = (0, 0, START)
bt = [pos]

index = 0

while index < len(bt):
    x, y, seed = bt[index]
    index += 1
    if (x, y) == (3, 3):
        logging.info(len(seed) - len(START))
        continue
    for direction in doors(seed):
        try:
            nx, ny = walk(x, y, direction)
            bt.append((nx, ny, seed + direction))
        except IndexError:
            pass
