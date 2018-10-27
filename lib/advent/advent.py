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
    def main(cls, *args, **kwargs):
        kwargs = {}
        try:
            arg1 = sys.argv[1]
        except:
            arg1 = 'input.txt'
        if os.path.isfile(arg1):
            kwargs['filename'] = arg1
        else:
            kwargs['data'] = arg1
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
            self.data = fh.read().strip()

    def solver(self, offset):
        pass

    def solve1(self):
        pass

    def solve2(self):
        pass

    def solve(self):
        print('solution 1: %s' % self.solve1())
        print('solution 2: %s' % self.solve2())