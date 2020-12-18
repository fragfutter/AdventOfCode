#!/usr/bin/pypy3

from advent import Advent
import re

"""
"""
ADD = '+'
MUL = '*'
NOP = None

def multiply(m):
    result = int(m.group(1)) * int(m.group(2))
    return str(result)

def add(m):
    result = int(m.group(1)) + int(m.group(2))
    return str(result)

def bracket(m):
    return calc(m.group(1))

def calc(data):
    current = data
    # brackets
    while True:
        reduced = re.sub(r'\(([\d*+ ]+)\)', bracket, current, count=1)
        if reduced == current:
            break
        current = reduced
    # add
    while True:
        reduced = re.sub(r'(\d+)\s*\+\s*(\d+)', add, current, count=1)
        if reduced == current:
            break
        current = reduced
    # multiply
    while True:
        reduced = re.sub(r'(\d+)\s*\*\s*(\d+)', multiply, current, count=1)
        if reduced == current:
            break
        current = reduced
    return current


class Day(Advent):
    lines = True

    def prepare1(self):
        result = []
        for line in self.data:
            # assume all single digits
            stack = []
            ops = []
            for token in line:
                if token == ' ':
                    continue
                if token in (ADD, MUL):
                    ops.append(token)
                elif token == '(':
                    ops.append(NOP)
                elif token == ')':
                    try:
                        op = ops.pop()
                        if op != NOP:
                            stack.append(op)
                    except IndexError:
                        pass
                else:
                    stack.append(int(token))
                    try:
                        op = ops.pop()
                        if op != NOP:
                            stack.append(op)
                    except IndexError:
                        pass
            assert(len(ops) == 0)
            result.append(stack)
        return result

    def solve1(self):
        result = 0
        for calc in self.prepare1():
            stack = []
            for token in calc:
                if token == ADD:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a + b)
                elif token == MUL:
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a * b)
                else:
                    stack.append(token)
            assert(len(stack) == 1)
            result += stack[0]
        return result

    def solve2(self):
        result = 0
        for line in self.data:
            result += int(calc(line))
        return result


Day.main()
