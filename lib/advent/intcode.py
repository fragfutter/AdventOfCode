import re
import operator
from threading import Thread, Event
from queue import Queue
from collections import defaultdict
import logging


POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2

OP_ADD = 1
OP_MULT = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_STOP = 99
OP_JUMP_TRUE = 5
OP_JUMP_FALSE = 6
OP_LESS = 7
OP_EQUAL = 8
OP_RELBASE = 9


class Intcode(Thread):
    def __init__(self, data, input_, output, name=None):
        super(Intcode, self).__init__(name=name)
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
            OP_RELBASE: (self.op_relbase, 1),
        }

        self.data = defaultdict(lambda: 0, enumerate(data))
        self.idx = 0
        self.input_ = input_
        self.output = output
        self.last_output = None
        self.relative_base = 0
        self.waiting_for_input = Event()

    def read(self, mode=None):
        """read current memory cell and advance by one,
        transform value according to mode"""
        result = self.data[self.idx]
        self.idx += 1
        if mode is None:
            return result
        if mode == POSITION_MODE:
            return self.data[result]
        if mode == IMMEDIATE_MODE:
            return result
        if mode == RELATIVE_MODE:
            return self.data[self.relative_base + result]
        raise Exception('unknown mode')


    def write(self, value, mode=None):
        """read current memory cell as target address
        and store value there"""
        address = self.read(None)
        if mode is None:
            pass
        elif mode == POSITION_MODE:
            pass
        elif mode == IMMEDIATE_MODE:
            pass
        elif mode == RELATIVE_MODE:
            address = self.relative_base + address
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
            args.append(self.read(mode))
        result = func(*args)
        if result is not None:
            mode = v % 10
            self.write(result, mode)

    def run(self):
        try:
            while True:
                self.step()
        except StopIteration:
            logging.debug('finished')
            pass

    def op_input(self):
        logging.debug('waiting for input')
        self.waiting_for_input.set()
        result = self.input_.get()
        logging.debug('got input %s', result)
        return result

    def op_output(self,  value):
        logging.debug('output %s', value)
        self.last_output = value
        self.output.put(value)

    def op_jump_true(self, value, target):
        if value != 0:
            self.idx = target

    def op_jump_false(self, value, target):
        if value == 0:
            self.idx = target

    def op_stop(self):
        raise StopIteration()

    def op_relbase(self, value):
        self.relative_base += value


def runit(data, *values):
    input_ = Queue()
    for v in values:
        input_.put(v)
    output = Queue()
    pc = Intcode(data, input_, output)
    pc.start()
    pc.join()
    return pc.last_output
