#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
import itertools
import sys
sys.setrecursionlimit(1000)

thulium = 1
plutonium = thulium << 1
strontium = plutonium << 1
promethium = strontium << 1
ruthenium = promethium << 1
hydrogen = ruthenium << 1
lithium = hydrogen << 1

elements = (thulium, plutonium, strontium, promethium, ruthenium, hydrogen, lithium)

# floor 0..3  [generators, chips]
# and in 4 we store [elevator, steps]

# NOTE; sorted tuples are much faster, they help in pruning BFS
data = [
    tuple(sorted((-thulium, thulium, -plutonium, -strontium))),
    tuple(sorted((plutonium,  strontium))),
    tuple(sorted((-promethium, promethium, -ruthenium, ruthenium))),
    tuple(),
]

data = (
    tuple(sorted((hydrogen, lithium))),
    tuple(sorted((-hydrogen,))),
    tuple(sorted((-lithium,))),
    tuple(),
)

directions = {
    0: (1,),
    1: (2, 0),
    2: (3, 1),
    3: (2,),
}


class State(object):
    def __init__(self, floors, elevator, step):
        self.elevator = elevator
        self.step = step
        self.floors = floors

    def __eq__(self, other):
        if self.elevator != other.elevator:
            return False
        # # different amount of elements on floors -> different
        # for a, b in zip(self.floors, other.floors):
        #     if len(a) != len(b):
        #         return False
        return \
            (self.elevator == other.elevator) and \
            (self.floors == other.floors)
        # # so now with remapping
        # # optimization, all elements are interchangeable

    def solution(self):
        # floors 0,1,2 empty
        return self.floors[0] == self.floors[1] == self.floors[2] == ()

    def validate(self):
        for floor in self.floors:
            if not floor:
                continue
            if floor[0] > 0:
                continue  # no generator, all chips are save
            if floor[-1] < 0:
                continue  # no chips also save
            for chip in filter(lambda x: x > 0, floor):
                if not -chip in floor:
                    return False  # unprotected chips found
        return True

    def moves(self):
        items = self.floors[self.elevator]
        return \
            list(itertools.combinations(items, 2)) + \
            list(itertools.combinations(items, 1))

    def generate(self):
        """generate all new states we can reach from us"""
        step = self.step + 1
        for direction in directions[self.elevator]:
            for items in self.moves():
                f = list(self.floors)
                f[self.elevator] = tuple(
                    x for x in self.floors[self.elevator]
                    if x not in items
                )
                f[direction] = tuple(sorted(
                    f[direction] +
                    items
                ))
                yield State(f, direction, step)

bfs = [State(data, 0, 0)]
searchposition = 0

while searchposition < len(bfs):
    current = bfs[searchposition]
    logging.debug('bfs width: %d, position: %d, depth: %d',
                  len(bfs), searchposition, current.step)
    for state in current.generate():
        if state.solution():
            logging.info('solution found in %d steps', state.step)
            sys.exit(0)
        if not state.validate():
            continue
        if state in bfs:
            continue
        bfs.append(state)
    searchposition += 1
