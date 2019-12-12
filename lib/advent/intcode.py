#!/usr/bin/pypy3

from advent import Advent
import re
import operator

"""
"""

POSITION_MODE = 0
IMMEDIATE_MODE = 1

OP_ADD = 1
OP_MULT = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_STOP = 99
OP_JUMP_TRUE = 5
OP_JUMP_FALSE = 6
OP_LESS = 7
OP_EQUAL = 8


class Intcode(object):
    def __init__(self, data, callback=None):
        self.ops = {
            OP_ADD: (operator.add, 2),
            OP_MULT: (operator.mul, 2),
            OP_INPUT: (self.op_input, 0),
            OP_OUTPUT: (self.op_output, 1),
            OP_STOP: (self.op_stop, 0),
            OP_JUMP_TRUE: (self.op_jump_true, 2),
            OP_JUMP_FALSE: (self.op_jump_false, 2),
            OP_LESS: (lambda a, b: int(a < b), 2),
            OP_EQUAL: (lambda a, b: int(a == b), 2),
        }

        self.data = data[:]
        self.idx = 0
        self.callback = callback
        self.last_output = None

    def read(self):
        """read current memory cell and advance by one"""
        result = self.data[self.idx]
        self.idx += 1
        return result

    def write(self, value):
        """read current memory cell as target address
        and store value there"""
        address = self.read()
        self.data[address] = value

    def step(self):
        """decode current register as instruction
        fetch required parameters, either immediate or
        position, run operation on parameters and store
        result"""
        v = self.read()
        op = v % 100
        v = int(v / 100)
        func, arg_count = self.ops[op]
        args = []
        for i in range(arg_count):
            mode = v % 10
            v = int(v / 10)
            register = self.read()
            if mode == POSITION_MODE:
                args.append(self.data[register])
            else:
                args.append(register)
        result = func(*args)
        if result is not None:
            self.write(result)

    def run(self):
        while True:
            self.step()

    def op_input(self):
        # expect use input
        value = self.callback()
        return value

    def op_output(self,  value):
        print('output: %s' % value)
        self.last_output = value

    def op_jump_true(self, value, target):
        if value != 0:
            self.idx = target

    def op_jump_false(self, value, target):
        if value == 0:
            self.idx = target

    def op_stop(self):
        raise StopIteration()