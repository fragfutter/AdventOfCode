#!/usr/bin/python

from functools import partial

from advent import Advent


"""
Permutation Promenade
---------------------

You come upon a very unusual sight; a group of programs here appear to be
dancing.

There are sixteen programs in total, named a through p. They start by standing
in a line: a stands in position 0, b stands in position 1, and so on until p,
which stands in position 15.

The programs' dance consists of a sequence of dance moves:

Spin, written sX, makes X programs move from the end to the front, but maintain
their order otherwise. (For example, s3 on abcde produces cdeab).  Exchange,
written xA/B, makes the programs at positions A and B swap places.
Partner, written pA/B, makes the programs named A and B swap places.

For example, with only five programs standing in a line (abcde), they could do
the following dance:

  * s1, a spin of size 1: eabcd.
  * x3/4, swapping the last two programs: eabdc.
  * pe/b, swapping programs e and b: baedc.
  * After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your puzzle
input). In what order are the programs standing after their dance?


Part Two
--------

Now that you're starting to get a feel for the dance moves, you turn your
attention to the dance as a whole.

Keeping the positions they ended up in from their previous dance, the programs
perform it again and again: including the first dance, a total of one billion
(1000000000) times.

In the example above, their second dance would begin with the order baedc, and
use the same dance moves:

  * s1, a spin of size 1: cbaed.
  * x3/4, swapping the last two programs: cbade.
  * pe/b, swapping programs e and b: ceadb.

In what order are the programs standing after their billion dances?
"""


class Day16(Advent):
    size = 16

    def reset(self):
        self.line = list([chr(ord('a') + i) for i in range(self.size)])

    def s(self, a):
        self.line = self.line[-a:] + self.line[:-a]
        return
        tmp = self.line + self.line
        self.line = tmp[-self.size-a:-a]

    def x(self, a, b):
        self.line[a], self.line[b] = self.line[b], self.line[a]

    def p(self, a, b):
        self.x(self.line.index(a), self.line.index(b))

    def prepare(self):
        super(Day16, self).prepare()
        self.reset()
        result = []
        for step in self.data.split(','):
            cmd = step[0]
            if cmd == 's':
                a = int(step[1:])
                result.append(partial(self.s, a))
            elif cmd == 'x':
                a, b = map(int, step[1:].split('/'))
                result.append(partial(self.x, a, b))
            elif cmd == 'p':
                a, b = step[1:].split('/')
                result.append(partial(self.p, a, b))
            else:
                raise Exception(step)
        self.data = result

    def solve1(self):
        self.reset()
        for step in self.data:
            step()
        return ''.join(self.line)

    def solve2(self):
        self.reset()
        seen = {}
        limit = 1000000000
        i = 0
        while i < limit:
            s = ''.join(self.line)
            if s in seen:
                # determine loop length
                loopsize = i - seen[s]
                print('loop detected size %d, fast forwarding' % loopsize)
                # forward in steps
                while i + loopsize < limit:
                    i += loopsize
                # wipe seen, so we execute all following steps until we
                # reach the limit
                seen = {}
            else:
                seen[s] = i
            for step in self.data:
                step()
            i += 1
        return ''.join(self.line)


Day16.main()
