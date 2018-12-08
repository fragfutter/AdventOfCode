#!/usr/bin/python

from advent import Advent


"""
Coprocessor Conflagration
-------------------------

You decide to head directly to the CPU and fix the printer from there. As you
get close, you find an experimental coprocessor doing so much work that the
local programs are afraid it will halt and catch fire. This would cause serious
issues for the rest of the computer, so you head in and see what you can do.

The code it's running seems to be a variant of the kind you saw recently on that
tablet. The general functionality seems very similar, but some of the
instructions are different:

  * set X Y sets register X to the value of Y.
  * sub X Y decreases register X by the value of Y.
  * mul X Y sets register X to the result of multiplying the value contained in
    register X by the value of Y.
  * jnz X Y jumps with an offset of the value of Y, but only if the value of X
    is not zero. (An offset of 2 skips the next instruction, an offset of -1
    jumps to the previous instruction, and so on.)

Only the instructions listed above are used. The eight registers here, named a
through h, all start at 0.

The coprocessor is currently set to some kind of debug mode, which allows for
testing, but prevents it from doing any meaningful work.

If you run the program (your puzzle input), how many times is the mul
instruction invoked?

Part Two
--------
Now, it's time to fix the problem.

The debug mode switch is wired directly to register a. You flip the switch,
which makes register a now start at 1 when the program is executed.

Immediately, the coprocessor begins to overheat. Whoever wrote this program
obviously didn't choose a very efficient implementation. You'll need to optimize
the program if it has any hope of completing before Santa needs that printer
working.

The coprocessor's ultimate goal is to determine the final value left in register
h once the program completes. Technically, if it had that... it wouldn't even
need to run the program.

After setting register a to 1, if the program were to run to completion, what
value would be left in register h?
"""


class Command(object):
    registers = dict([(i, 0) for i in 'abcdefgh'])
    mulcount = 0

    def __init__(self, data):
        self.debug = data
        self.cmd, self.a, self._b = data.split(' ')
        try:
            self._b = int(self._b)
        except ValueError:
            pass

    def exec_(self):
        return getattr(self, self.cmd)()

    @property
    def b(self):
        try:
            return Command.registers[self._b]
        except KeyError:
            return self._b

    def set(self):
        Command.registers[self.a] = self.b
        if self.a == 'h':
            print(Command.registers[self.a])
        return 1

    def sub(self):
        Command.registers[self.a] -= self.b
        return 1

    def mul(self):
        Command.registers[self.a] *= self.b
        Command.mulcount += 1
        return 1

    def jnz(self):
        try:
            val = Command.registers[self.a]
        except KeyError:
            val = int(self.a)
        if val != 0:
            return self.b
        else:
            return 1


class Day23(Advent):
    lines = True
    conversion = Command

    def prepare(self):
        super(Day23, self).prepare()

    def solve1(self):
        pos = 0
        while True:
            if pos >= len(self.data):
                break
            cmd = self.data[pos]
            pos += cmd.exec_()
        return Command.mulcount

    def solve2(self):
        Command.registers = dict([(i, 0) for i in 'abcdefgh'])
        Command.registers['a'] = 1
        pos = 0
        while True:
            if pos >= len(self.data):
                break
            cmd = self.data[pos]
            pos += cmd.exec_()
        return Command.mulcount

Day23.main()
