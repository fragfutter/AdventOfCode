#!/usr/bin/python

import numpy as np
from advent import Advent


"""
Fractal Art
-----------
You find a program trying to generate some art. It uses a strange process that
involves repeatedly enhancing the detail of an image through a set of rules.

The image consists of a two-dimensional square grid of pixels that are either on
(#) or off (.). The program always begins with this pattern:

  .#.
  ..#
  ###

Because the pattern is both 3 pixels wide and 3 pixels tall, it is said to have
a size of 3.

Then, the program repeats the following process:

If the size is evenly divisible by 2, break the pixels up into 2x2 squares, and
convert each 2x2 square into a 3x3 square by following the corresponding
enhancement rule.  Otherwise, the size is evenly divisible by 3; break the
pixels up into 3x3 squares, and convert each 3x3 square into a 4x4 square by
following the corresponding enhancement rule.

Because each square of pixels is replaced by a larger one, the image gains
pixels and so its size increases.

The artist's book of enhancement rules is nearby (your puzzle input); however,
it seems to be missing rules. The artist explains that sometimes, one must
rotate or flip the input pattern to find a match. (Never rotate or flip the
output pattern, though.) Each pattern is written concisely: rows are listed as
single units, ordered top-down, and separated by slashes. For example, the
following rules correspond to the adjacent patterns:

  ../.#  =  ..
            .#

                  .#.
  .#./..#/###  =  ..#
                  ###

                          #..#
  #..#/..../#..#/.##.  =  ....
                          #..#
                          .##.

When searching for a rule to use, rotate and flip the pattern as necessary. For
example, all of the following patterns match the same rule:

  .#.   .#.   #..   ###
  ..#   #..   #.#   ..#
  ###   ###   ##.   .#.

Suppose the book contained the following two rules:

  ../.# => ##./#../...
  .#./..#/### => #..#/..../..../#..#

As before, the program begins with this pattern:

.#.
..#
###

The size of the grid (3) is not divisible by 2, but it is divisible by 3. It
divides evenly into a single square; the square matches the second rule, which
produces:

  #..#
  ....
  ....
  #..#

The size of this enhanced grid (4) is evenly divisible by 2, so that rule is
used. It divides evenly into four squares:

  #.|.#
  ..|..
  --+--
  ..|..
  #.|.#

Each of these squares matches the same rule (../.# => ##./#../...), three of
which require some flipping and rotation to line up with the rule. The output
for the rule is the same in all four cases:

  ##.|##.
  #..|#..
  ...|...
  ---+---
  ##.|##.
  #..|#..
  ...|...

Finally, the squares are joined into a new grid:

  ##.##.
  #..#..
  ......
  ##.##.
  #..#..
  ......

Thus, after 2 iterations, the grid contains 12 pixels that are on.

How many pixels stay on after 5 iterations?

Part Two
--------
How many pixels stay on after 18 iterations?
"""


def str_to_array(data):
    """convert single line representation to numpy array
    #./..  becomes array([[1,0], [0,0]])
    """
    data = data.split('/')
    data = [
        [x == '#' for x in row]
        for row in data
    ]
    return np.array(data)


class Pattern(object):
    def __init__(self, line):
        in_, out_ = line.split(' => ')
        self.out = str_to_array(out_)
        self.in_ = self.equivalents(str_to_array(in_))

    def equivalents(self, p):
        """mutate the in pattern"""
        result = []
        for i in range(4):
            result.append(p)
            result.append(np.fliplr(p))
            result.append(np.flipud(p))
            p = np.rot90(p)
        return result


class Fractal(object):
    def __init__(self, rules, seed='.#./..#/###'):
        self.rules = rules
        self.data = str_to_array(seed)

    @property
    def slicer(self):
        if len(self.data) % 2 == 0:
            return 2
        else:
            return 3

    @property
    def size(self):
        return len(self.data)

    def subs(self):
        """return subarrays"""
        s = self.slicer
        for x in range(0, self.size, s):
            for y in range(0, self.size, s):
                yield self.data[y:y+s, x:x+s]
            yield None  # mark end of row

    def mutate_sub(self, sub):
        for rule in self.rules:
            for k in rule.in_:
                if np.array_equal(sub, k):
                    return rule.out.copy()
        raise AssertionError('no rule matched')

    def mutate(self):
        result = []
        row = []
        for sub in self.subs():
            if sub is None:
                result.append(np.concatenate(np.array(row)))
                row = []
                continue
            row.append(self.mutate_sub(sub))
        self.data = np.concatenate(result, axis=1)

    def dump(self):
        for row in self.data:
            print(''.join(['#' if x else '.' for x in row]))

    def count(self):
        return np.count_nonzero(self.data)


class Day21(Advent):
    lines = True
    conversion = Pattern

    def prepare(self):
        super(Day21, self).prepare()

    def solver(self):
        result = []
        fractal = Fractal(self.data)
        for i in range(18):
            print(i)
            fractal.mutate()
            if i == 4:
                result.append(fractal.count())
            if i == 17:
                result.append(fractal.count())
        return result


Day21.main()
