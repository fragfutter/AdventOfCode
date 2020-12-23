#!/usr/bin/pypy3

from advent import Advent
import logging

"""
"""
# use a linked list
class Cup(object):
    def __init__(self, label, next_=None):
        self.label = label
        self.next_ = next_

    def __eq__(self, other):
        return self.label == other.label

    def insert(self, cup):
        """insert cup after self"""
        cup.next_ = self.next_
        self.next_ = cup

    def pop(self):
        """remove and return the cup after self"""
        result = self.next_
        self.next_ = result.next_
        result.next_ = None
        return result


class Day(Advent):
    def prepare(self):
        self.data = list(map(int, self.data))

    def play(self, labels, turns):
        maxlabel = max(labels)
        lookup = {}  # label -> cup-object
        previous = None
        for label in labels:
            cup = Cup(label)
            if previous:
                previous.next_ = cup
            previous = cup
            lookup[label] = cup
        # make it a circle
        lookup[labels[-1]].next_ = lookup[labels[0]]
        # position start
        current = lookup[labels[0]]
        for i in range(turns):
            buf = []
            for i in range(3):
                buf.append(current.pop())
            dest = current.label - 1
            while dest < 1 or lookup[dest] in buf:
                dest = dest -1
                if dest < 1:
                    dest = maxlabel
            # insert after cup with destination label
            for c in reversed(buf):
                lookup[dest].insert(c)
            current = current.next_
        return lookup[1]

    def solve1(self):
        cup_one = self.play(self.data, 100)
        result = []
        cup = cup_one.next_
        while cup != cup_one:
            result.append(cup.label)
            cup = cup.next_
        return ''.join(map(str, result))

    def solve2(self):
        labels = self.data[:]
        labels.extend(list(range(max(labels) + 1, 1000000 + 1 )))
        cup_one = self.play(labels, 10000000)
        a = cup_one.next_
        b = a.next_
        return a.label * b.label

logging.basicConfig(level=logging.INFO)
Day.main()
