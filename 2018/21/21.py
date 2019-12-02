#!/usr/bin/python

import pdb
from itertools import count

from advent import Advent

"""
--- Day 21: Chronal Conversion ---
You should have been watching where you were going, because as you wander the
new North Pole base, you trip and fall into a very deep hole!

Just kidding. You're falling through time again.

If you keep up your current pace, you should have resolved all of the temporal
anomalies by the next time the device activates. Since you have very little
interest in browsing history in 500-year increments for the rest of your life,
you need to find a way to get back to your present time.

After a little research, you discover two important facts about the behavior of
the device:

First, you discover that the device is hard-wired to always send you back in
time in 500-year increments. Changing this is probably not feasible.

Second, you discover the activation system (your puzzle input) for the time
travel module. Currently, it appears to run forever without halting.

If you can cause the activation system to halt at a specific moment, maybe you
can make the device send you so far back in time that you cause an integer
underflow in time itself and wrap around back to your current time!

The device executes the program as specified in manual section one and manual
section two.

Your goal is to figure out how the program works and cause it to halt. You can
only control register 0; every other register begins at 0 as usual.

Because time travel is a dangerous activity, the activation system begins with a
few instructions which verify that bitwise AND (via bani) does a numeric
operation and not an operation as if the inputs were interpreted as strings. If
the test fails, it enters an infinite loop re-running the test instead of
allowing the program to execute normally. If the test passes, the program
continues, and assumes that all other bitwise operations (banr, bori, and borr)
also interpret their inputs as numbers. (Clearly, the Elves who wrote this
system were worried that someone might introduce a bug while trying to emulate
this system with a scripting language.)

What is the lowest non-negative integer value for register 0 that causes the
program to halt after executing the fewest instructions? (Executing the same
instruction multiple times counts as multiple instructions executed.) """


class Cpu(object):
    funcs = [
        'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
        'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr',
    ]

    def __init__(self, initial=[0, 0, 0, 0, 0, 0]):
        self.registers = initial[:]

    def addr(self, a, b, c):
        self.registers[c] = self.registers[a] + self.registers[b]

    def mulr(self, a, b, c):
        self.registers[c] = self.registers[a] * self.registers[b]

    def banr(self, a, b, c):
        self.registers[c] = self.registers[a] & self.registers[b]

    def borr(self, a, b, c):
        self.registers[c] = self.registers[a] | self.registers[b]

    def setr(self, a, b, c):
        self.registers[c] = self.registers[a]

    def addi(self, a, b, c):
        self.registers[c] = self.registers[a] + b

    def muli(self, a, b, c):
        self.registers[c] = self.registers[a] * b

    def bani(self, a, b, c):
        self.registers[c] = self.registers[a] & b

    def bori(self, a, b, c):
        self.registers[c] = self.registers[a] | b

    def seti(self, a, b, c):
        self.registers[c] = a

    def gtir(self, a, b, c):
        self.registers[c] = int(a > self.registers[b])

    def eqir(self, a, b, c):
        self.registers[c] = int(a == self.registers[b])

    def gtri(self, a, b, c):
        self.registers[c] = int(self.registers[a] > b)

    def eqri(self, a, b, c):
        self.registers[c] = int(self.registers[a] == b)

    def gtrr(self, a, b, c):
        self.registers[c] = int(self.registers[a] > self.registers[b])

    def eqrr(self, a, b, c):
        self.registers[c] = int(self.registers[a] == self.registers[b])

    @classmethod
    def test_instruction(cls, before=None, after=None, op=None, args=None,
                         funcs=None):
        result = []
        if funcs is None:
            funcs = cls.funcs
        for f in funcs:
            cpu = Cpu(before)
            getattr(cpu, f)(*args)
            if cpu.registers == after:
                result.append(f)
        return result


class Day(Advent):
    lines = True

    def prepare(self):
        super(Day, self).prepare()
        cpu = Cpu()
        code = []
        for line in self.data:
            if line.startswith('#'):
                self.ipreg = int(line[4:])
            else:
                data = line.split(' ')
                f = data.pop(0)
                f = getattr(cpu, f)
                args = [int(x) for x in data]
                code.append((f, args))
        self.cpu = cpu
        self.code = code

    def runner(self, regs):
        cpu = self.cpu
        cpu.registers = regs
        ip = 0
        ipreg = self.ipreg
        for i in count():
            if ip < 0 or ip >= len(self.code):
                break
            cpu.registers[ipreg] = ip
            # used this to detect the loop: print(ip)
            # loop is 3 to 11
            if ip == 2:
                print(cpu.registers)
                # [1, 5, 0, 2, 10551368, 10551367]
                # [1, 6, 0, 2, 10551368, 10551367]
                # [1, 7, 0, 2, 10551368, 10551367]
                # [1, 8, 0, 2, 10551368, 10551367]
                #
            f, args = self.code[ip]
            log.debug('%02d: %s %s', ip, f, args)
            log.debug('  :registers %s', cpu.registers)
            f(*args)
            log.debug('  :registers %s', cpu.registers)
            ip = cpu.registers[ipreg]
            ip += 1
            pdb.set_trace()

    def solve1(self):
        return self.runner([1000000000000000000, 0, 0, 0, 0, 0])

    def solve2(self):
        pass


Day.main()
