#!/usr/bin/pypy3

from advent import Advent

"""
"""

class Machine(object):
    def __init__(self):
        self.accumulator = 0
        self.instructions = []
        self.pointer = 0

    def step(self):
        """execute one instruction
        return new pointer position, current accumulator, previous accumulator
        """
        last = self.accumulator
        op, arg = self.instructions[self.pointer]
        if op == 'acc':
            self.accumulator += arg
            self.pointer += 1
        elif op == 'jmp':
            self.pointer += arg
        elif op == 'nop':
            self.pointer += 1
        else:
            raise Exception('unknown operator "%s"' % op)
        return self.pointer, self.accumulator, last

    def append(self, op, val):
        """add instruction"""
        self.instructions.append((op, val))

    def reset(self):
        self.pointer = 0
        self.accumulator = 0

    def run_loopcheck(self):
        self.reset()
        seen = []
        while True:
            p, c, l = self.step()
            if p in seen:
                return l
            seen.append(p)

    def run_termination(self):
        try:
            self.run_loopcheck()
        except IndexError:
            if self.pointer == len(self.instructions):
                return True
        return False

    def clone(self):
        result = Machine()
        for op, val in self.instructions:
            result.append(op, val)
        return result


class Day(Advent):
    def prepare(self):
        result = Machine()
        for line in self.data.split('\n'):
            line = line.strip()
            op, val = line.split(' ')
            val = int(val)
            result.append(op, val)
        self.data = result

    def solve1(self):
        return self.data.run_loopcheck()

    def solve2(self):
        pos = len(self.data.instructions)
        while True:
            machine = self.data.clone()
            # modify one jmp/nop, starting at the end ;)
            while True:
                pos -= 1
                op, val = machine.instructions[pos]
                if op == 'jmp':
                    machine.instructions[pos] = ('nop', val)
                    break
                elif op == 'nop':
                    machine.instructions[pos] = ('jmp', val)
                    break
            if machine.run_termination():
                return machine.accumulator


Day.main()
