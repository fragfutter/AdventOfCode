#!/usr/bin/python

from advent import Advent

"""
--- Day 16: Chronal Classification ---
As you see the Elves defend their hot chocolate successfully, you go back to
falling through time. This is going to become a problem.

If you're ever going to return to your own time, you need to understand how this
device on your wrist works. You have a little while before you reach your next
destination, and with a bit of trial and error, you manage to pull up a
programming manual on the device's tiny screen.

According to the manual, the device has four registers (numbered 0 through 3)
that can be manipulated by instructions containing one of 16 opcodes. The
registers start with the value 0.

Every instruction consists of four values: an opcode, two inputs (named A and
B), and an output (named C), in that order. The opcode specifies the behavior of
the instruction and how the inputs are interpreted. The output, C, is always
treated as a register.

In the opcode descriptions below, if something says "value A", it means to take
the number given as A literally. (This is also called an "immediate" value.) If
something says "register A", it means to use the number given as A to read from
(or write to) the register with that number. So, if the opcode addi adds
register A and value B, storing the result in register C, and the instruction
addi 0 7 3 is encountered, it would add 7 to the value contained by register 0
and store the sum in register 3, never modifying registers 0, 1, or 2 in the
process.

Many opcodes are similar except for how they interpret their arguments. The
opcodes fall into seven general categories:

Addition:

  - addr (add register) stores into register C the result of adding register A
  and register B.
  - addi (add immediate) stores into register C the result of adding register A
  and value B.

Multiplication:

  - mulr (multiply register) stores into register C the result of multiplying
  register A and register B.
  - muli (multiply immediate) stores into register C the result of multiplying
  register A and value B.

Bitwise AND:

  - banr (bitwise AND register) stores into register C the result of the bitwise
  AND of register A and register B.
  - bani (bitwise AND immediate) stores into register C the result of the
  bitwise AND of register A and value B.

Bitwise OR:

  - borr (bitwise OR register) stores into register C the result of the bitwise
  OR of register A and register B.
  - bori (bitwise OR immediate) stores into register C the result of the bitwise
  OR of register A and value B.

Assignment:

  - setr (set register) copies the contents of register A into register C.
  (Input B is ignored.)
  - seti (set immediate) stores value A into register C. (Input B is ignored.)

Greater-than testing:

  - gtir (greater-than immediate/register) sets register C to 1 if value A is
  greater than register B. Otherwise, register C is set to 0.
  - gtri (greater-than register/immediate) sets register C to 1 if register A is
  greater than value B. Otherwise, register C is set to 0.
  - gtrr (greater-than register/register) sets register C to 1 if register A is
  greater than register B. Otherwise, register C is set to 0.

Equality testing:

  - eqir (equal immediate/register) sets register C to 1 if value A is equal to
  register B. Otherwise, register C is set to 0.
  - eqri (equal register/immediate) sets register C to 1 if register A is equal
  to value B. Otherwise, register C is set to 0.
  - eqrr (equal register/register) sets register C to 1 if register A is equal
  to register B. Otherwise, register C is set to 0.

Unfortunately, while the manual gives the name of each opcode, it doesn't seem
to indicate the number.  However, you can monitor the CPU to see the contents of
the registers before and after instructions are executed to try to work them
out. Each opcode has a number from 0 through 15, but the manual doesn't say
which is which. For example, suppose you capture the following sample:

Before: [3, 2, 1, 1]
9 2 1 2
After:  [3, 2, 2, 1]

This sample shows the effect of the instruction 9 2 1 2 on the registers. Before
the instruction is executed, register 0 has value 3, register 1 has value 2, and
registers 2 and 3 have value 1. After the instruction is executed, register 2's
value becomes 2.

The instruction itself, 9 2 1 2, means that opcode 9 was executed with A=2, B=1,
and C=2. Opcode 9 could be any of the 16 opcodes listed above, but only three of
them behave in a way that would cause the result shown in the sample:

  - Opcode 9 could be mulr: register 2 (which has a value of 1) times register 1
  (which has a value of 2) produces 2, which matches the value stored in the
  output register, register 2.
  - Opcode 9 could be addi: register 2 (which has a value of 1) plus value 1
  produces 2, which matches the value stored in the output register, register 2.
  - Opcode 9 could be seti: value 2 matches the value stored in the output
  register, register 2; the number given for B is irrelevant.

None of the other opcodes produce the result captured in the sample. Because of
this, the sample above behaves like three opcodes.

You collect many of these samples (the first section of your puzzle input). The
manual also includes a small test program (the second section of your puzzle
input) - you can ignore it for now.

Ignoring the opcode numbers, how many samples in your puzzle input behave like
three or more opcodes?

--- Part Two ---
Using the samples you collected, work out the number of each opcode and execute
the test program (the second section of your puzzle input).
"""


class Cpu(object):
    funcs = [
        'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
        'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr',
    ]

    def __init__(self, initial=[0, 0, 0, 0]):
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
        # split into samples and program
        samples = []
        program = []
        instruction = {}
        for line in self.data:
            if not line:
                continue
            if line.startswith('Before:'):
                instruction['before'] = \
                    list(map(int, line.split(': ')[1][1:-1].split(', ')))
            elif line.startswith('After:'):
                instruction['after'] = \
                    list(map(int, line.split(':  ')[1][1:-1].split(', ')))
            else:
                v = list(map(int, line.split(' ')))
                instruction['op'] = v.pop(0)
                instruction['args'] = v
            if 'after' in instruction:
                samples.append(instruction)
                instruction = {}
            if 'op' in instruction and 'before' not in instruction:
                program.append(instruction)
                instruction = {}
        self.samples = samples
        self.program = program

    def solve1(self):
        result = 0
        for sample in self.samples:
            hits = Cpu.test_instruction(**sample)
            if len(hits) >= 3:
                result += 1
        return result

    def solve2(self):
        codes = {}
        for i in range(16):
            codes[i] = Cpu.funcs[:]
        for sample in self.samples:
            op = sample['op']
            funcs = codes[op]  # possible candidates
            codes[op] = Cpu.test_instruction(funcs=funcs, **sample)
            # if we became unique, remove us from all others
            if len(codes[op]) == 1:
                f = codes[op][0]
                for other, funcs in codes.items():
                    if other == op:
                        continue
                    if f in funcs:
                        funcs.remove(f)
        # run the program
        cpu = Cpu()
        for instruction in self.program:
            op = instruction['op']
            # translate
            f = codes[op][0]
            args = instruction['args']
            getattr(cpu, f)(*args)
        return cpu.registers[0]


Day.main()
