#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
import itertools
import copy
import sys
sys.setrecursionlimit(1000)

data = [
    ['tg', 'tc', 'pg', 'sg'],
    ['pc', 'sc'],
    ['Pg', 'Pc', 'rg', 'rc'],
    [],
]
min_steps = 10


def validate(floors):
    for floor in floors:
        # split into chips and generators
        chips = [y[0] for y in filter(lambda x: x[1] == 'c', floor)]
        generators = [y[0] for y in filter(lambda x: x[1] == 'g', floor)]
        unprotected = []
        for chip in chips:
            if chip in generators:
                continue
            else:
                unprotected.append(chip)
        if unprotected and generators:
            # chips without generator left
            return False
    return True


def solution(floors):
    for floor in floors[:len(floors) - 1]:
        if len(floor) > 0:
            return False
    print(min_steps)
    return True


def itemiter(data):
    for i in data:
        yield (i, )
    for i in itertools.combinations(data, 2):
        if i[0][0] == i[1][0]:
            yield i  # matching generator and chip
        elif i[0][1] == i[1][1]:
            yield i  # both chips or both generators


def moves(floors, elevator):
    """generate all possible moves"""
    # only move one up or one down
    # we need to stop on each floor anyway
    for e in (elevator + 1, elevator - 1):
        if e < 0 or e >= len(floors):
            continue
        for items in itemiter(floors[elevator]):
            f = copy.deepcopy(floors)
            for item in items:
                f[elevator].remove(item)
                f[e].append(item)
            if validate(f):
                yield f, e


def branch(floors, elevator, step):
    global min_steps
    step += 1
    for f, e in moves(floors, elevator):
        if solution(f):
            if step < min_steps:
                min_steps = step
        else:
            if step < min_steps:
                branch(f, e, step)


branch(data, 0, 0)
print(min_steps)
