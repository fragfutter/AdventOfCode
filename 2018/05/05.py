#!/usr/bin/python

import re
import string

from advent import Advent

"""
--- Day 5: Alchemical Reduction ---
You've managed to sneak in to the prototype suit manufacturing lab. The Elves
are making decent progress, but are still struggling with the suit's size
reduction capabilities.

While the very latest in 1518 alchemical technology might have solved their
problem eventually, you can do better. You scan the chemical composition of the
suit's material and discover that it is formed by extremely long polymers (one
of which is available as your puzzle input).

The polymer is formed by smaller units which, when triggered, react with each
other such that two adjacent units of the same type and opposite polarity are
destroyed. Units' types are represented by letters; units' polarity is
represented by capitalization. For instance, r and R are units with the same
type but opposite polarity, whereas r and s are entirely different types and do
not react.

For example:

  In aA, a and A react, leaving nothing behind.
  In abBA, bB destroys itself, leaving aA. As above, this then destroys itself,
    leaving nothing.
  In abAB, no two adjacent units are of the same type, and so nothing happens.
  In aabAAB, even though aa and AA are of the same type, their polarities match,
    and so nothing happens.

Now,consider a larger example, dabAcCaCBAcCcaDA:


  dabAcCaCBAcCcaDA  The first 'cC' is removed.
  dabAaCBAcCcaDA    This creates 'Aa', which is removed.
  dabCBAcCcaDA      Either 'cC' or 'Cc' are removed (the result is the same).
  dabCBAcaDA        No further actions can be taken.

After all possible reactions, the resulting polymer contains 10 units.

How many units remain after fully reacting the polymer you scanned?

--- Part Two ---
Time to improve the polymer.

One of the unit types is causing problems; it's preventing the polymer from
collapsing as much as it should. Your goal is to figure out which unit type is
causing the most problems, remove all instances of it (regardless of polarity),
fully react the remaining polymer, and measure its length.

For example, again using the polymer dabAcCaCBAcCcaDA from above:

  Removing all A/a units produces dbcCCBcCcD. Fully reacting this polymer
    produces dbCBcD, which has length 6.
  Removing all B/b units produces daAcCaCAcCcaDA. Fully reacting this polymer
    produces daCAcaDA, which has length 8.
  Removing all C/c units produces dabAaBAaDA. Fully reacting this polymer
    produces daDA, which has length 4.
  Removing all D/d units produces abAcCaCBAcCcaA. Fully reacting this polymer
    produces abCBAc, which has length 6.

In this example, removing all C/c units was best, producing the answer 4.

What is the length of the shortest polymer you can produce by removing all units
of exactly one type and fully reacting the result?

"""


class Day(Advent):
    lines = False

    def prepare(self):
        super(Day, self).prepare()
        # create all reactions
        result = []
        for a, A in zip(string.ascii_lowercase, string.ascii_uppercase):
            result.append(a + A)
            result.append(A + a)
        self.reactions = result
        # same with a regular expression
        pat = []
        for a, A in zip(string.ascii_lowercase, string.ascii_uppercase):
            pat.append(a + A)
            pat.append(A + a)
        pat = '(%s)' % '|'.join(pat)
        self.pattern = re.compile(pat)

    ###
    # Solving with loops
    ###

    def react(self, poly):
        poly = ''.join([
            part for part in
            [poly[i:i+2] for i in range(0, len(poly), 2)]
            if part not in self.reactions
        ])
        # and now with an offset
        poly = ' ' + poly
        poly = ''.join([
            part for part in
            [poly[i:i+2] for i in range(0, len(poly), 2)]
            if part not in self.reactions
        ])
        return poly[1:]  # remove offset

    def fullreact_(self, poly):
        size = 0
        while True:
            size = len(poly)
            poly = self.react(poly)
            if size == len(poly):
                break
        return size

    ###
    # solving with regexp
    ###
    def fullreact(self, poly):
        matched = True
        while matched:
            poly, matched = self.pattern.subn('', poly)
        return len(poly)

    def solve1(self):
        return self.fullreact(self.data)

    def solve2(self):
        result = []
        for a in string.ascii_lowercase:
            poly = re.sub(a, '', self.data, flags=re.I)
            length = self.fullreact(poly)
            print(a, self.fullreact(poly))
            result.append(length)
        return min(result)


Day.main()
