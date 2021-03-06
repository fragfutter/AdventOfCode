import sys
import os
import re


class Advent(object):
    """
    subclass this to implement a adventofcode solver

    automaticly loads data from input.txt and stores it in self.data

    calls prepare to reformat the data (implement if necessary)

    calls solve1 and solve2 to solve the two parts of the puzzle

    and a classmethod main to run it

    ..code python::

        Advent.main()
    """

    lines = False  #: is the input line based? If true split a newline
    matrix = False  #: input is a 2D array seperated by seperator
    strip = True  #: strip whitespace from each input token
    conversion = None  #: conversion function for each token, for example int
    seperator = re.compile('\s+')

    @classmethod
    def find_input(cls, *args):
        candidates = []
        try:
            candidates.append(sys.argv[1])
        except:
            pass  # no input given
        c = os.path.basename(sys.argv[0])
        candidates.append(os.path.splitext(c)[0] + '.txt')
        candidates.append('input.txt')
        candidates.append('sample.txt')
        for c in candidates:
            if os.path.isfile(c):
                return c

    @classmethod
    def main(cls, *args, **kwargs):
        filename = cls.find_input(*args)
        if filename:
            kwargs['filename'] = filename
        else:
            kwargs['data'] = sys.argv[1]
        advent = cls(**kwargs)
        advent.solve()

    def __init__(self, data=None, filename=None, **kwargs):
        if filename:
            self.load(filename)
        else:
            self.data = data
        self.prepare()

    def prepare(self):
        if self.lines or self.matrix:
            self.data = self.data.split('\n')
        if self.matrix:
            self.data = [self.seperator.split(line) for line in self.data]
        if self.strip:
            if self.matrix:
                self.data = [
                    [x.strip() for x in row]
                    for row in self.data
                ]
            elif self.lines:
                self.data = [x.strip() for x in self.data]
            else:
                self.data = self.data.strip()
        if self.conversion:
            if self.matrix:
                self.data = [
                    [self.conversion(x) for x in row]
                    for row in self.data
                ]
            elif self.lines:
                self.data = [self.conversion(x) for x in self.data]
            else:
                self.data = self.conversion(self.data)

    def load(self, filename):
        with open(filename) as fh:
            self.data = fh.read()
            if self.strip:
                self.data = self.data.strip()

    def solver(self):
        """implement this to return a tuple with both solutions"""
        return self.solve1(), self.solve2()

    def solve1(self):
        return None

    def solve2(self):
        return None

    def solve(self):
        s1, s2 = self.solver()
        print('solution 1: %s' % s1)
        print('solution 2: %s' % s2)
