#!/usr/bin/pypy3

from advent import Advent

"""
--- Day 4: Secure Container ---
You arrive at the Venus fuel depot only to discover it's protected by a
password. The Elves had written the password on a sticky note, but someone threw
it out.

However, they do remember a few key facts about the password:

- It is a six-digit number.
- The value is within the range given in your puzzle input.
- Two adjacent digits are the same (like 22 in 122345).
- Going from left to right, the digits never decrease; they only ever increase
  or stay the same (like 111123 or 135679).

Other than the range rule, the following are true:

- 111111 meets these criteria (double 11, never decreases).
- 223450 does not meet these criteria (decreasing pair of digits 50).
- 123789 does not meet these criteria (no double).

How many different passwords within the range given in your puzzle input meet
these criteria?

--- Part Two ---
An Elf just remembered one more important detail: the two adjacent matching
digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the
following are now true:

- 112233 meets these criteria because the digits never decrease and all repeated
  digits are exactly two digits long.
- 123444 no longer meets the criteria (the repeated 44 is part of a larger group
  of 444).
- 111122 meets the criteria (even though 1 is repeated more than twice, it still
  contains a double 22).

How many different passwords within the range given in your puzzle input meet
all of the criteria?
"""

class Day(Advent):
    lines = True
    conversion = int

    def generate(self, two=False):
        for a in range(1, 9+1):
            for b in range(a, 9+1):
                for c in range(b, 9+1):
                    for d in range(c, 9+1):
                        for e in range (d, 9+1):
                            for f in range(e, 9+1):
                                if not (a==b or b==c or c==d or d==e or e==f):
                                    continue
                                if two and not (\
                                        (a==b and b!=c) or \
                                        (b==c and a!=b and c!=d) or \
                                        (c==d and b!=c and d!=e) or \
                                        (d==e and c!=d and e!=f) or \
                                        (e==f and d!=e)\
                                                ):
                                    continue
                                yield \
                                    a * 100000 + \
                                    b * 10000 + \
                                    c * 1000 + \
                                    d * 100 + \
                                    e * 10 + \
                                    f

    def solve1(self):
        min_ , max_ = self.data
        candidates = filter(lambda x: x > min_ and x < max_, self.generate())
        return len(list(candidates))

    def solve2(self):
        min_ , max_ = self.data
        candidates = filter(lambda x: x > min_ and x < max_, self.generate(True))
        return len(list(candidates))


Day.main()
