#!/usr/bin/python

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
import itertools
import sys


class Day21(object):
    mapping = {
        'swap position': (2, 5),
        'swap letter': (2, 5),
        'reverse': (2, 4),
        'rotate left': (2,),
        'rotate right': (2,),
        'rotate based': (6,),
        'reverse': (2, 4),
        'move': (2, 5),
    }

    def __init__(self, data):
        self.data = list(data)

    def swap_position(self, x, y):
        y1 = self.data[y]
        self.data[y] = self.data[x]
        self.data[x] = y1

    def swap_letter(self, x, y):
        for i in range(len(self.data)):
            if self.data[i] == x:
                self.data[i] = y
            elif self.data[i] == y:
                self.data[i] = x

    def rotate(self, steps):
        self.data = self.data[steps:] + self.data[:steps]

    def rotate_left(self, steps):
        self.rotate(steps)

    def rotate_right(self, steps):
        self.rotate(len(self.data) - steps)

    def rotate_based(self, letter):
        i = self.data.index(letter)
        if i >= 4:
            i += 1
        i += 1
        self.rotate_right(i)

    def reverse(self, x, y):
        y += 1
        pre, mid, end = self.data[:x], self.data[x:y], self.data[y:]
        self.data = pre + mid[::-1] + end

    def move(self, x, y):
        l = self.data[x]
        del self.data[x]
        self.data.insert(y, l)

    def do(self, line):
        logging.debug('processing %s', line)
        t = line.split(' ')
        for k, v in self.mapping.items():
            if line.startswith(k):
                func = getattr(self, '_'.join(k.split(' ')))
                args = []
                for i in v:
                    a = t[i]
                    try:
                        a = int(a)
                    except ValueError:
                        pass
                    args.append(a)
                func(*args)
                logging.debug(self.data)
                break

    def scramble(self, filename):
        fh = open(filename, 'r')
        for line in fh.readlines():
            self.do(line.strip())
        fh.close()

    def undo(self, line):
        t = line.split(' ')
        if line.startswith('swap position'):
            self.swap_position(int(t[2]), int(t[5]))
        elif line.startswith('swap letter'):
            self.swap_letter(t[2], t[5])
        elif line.startswith('rotate left'):
            self.rotate_right(int(t[2]))
        elif line.startswith('rotate right'):
            self.rotate_left(int(t[2]))
        elif line.startswith('rotate based'):
            # TODO
            # each letter only once
            # so we can prepare an undo table
            # based on the current position of the letter
            # 10000000 (0) => 01000000 (1)
            # 01000000 (1) => 00010000 (4)
            # ...
            # this works for the given 8 charater
            # see gen_rotate_base_reverse below
            # but not for other lengths, so leaving it
            # and staying with brute force
            sys.exit(1)
            self.swap_position(int(t[2]), int(t[5]))
        elif line.startswith('reverse'):
            self.reverse(int(t[2]), int(t[4]))
        elif line.startswith('move'):
            self.move(int(t[2]), int(t[5]))


def gen_rotate_base_reverse():
    SIZE = len('abcdefgh')
    result = {}
    for i in range(SIZE):
        test = ['a', ] * SIZE
        test[i] = 'b'
        day = Day21(''.join(test))
        day.rotate_based('b')
        r = day.data.index('b')
        assert(r not in result.keys())
        result[r] = i
    logging.info(result)
    sys.exit(0)

# part1
day = Day21('abcdefgh')
day.scramble('input_21.txt')
print(''.join(day.data))

# part2 brute force
for p in itertools.permutations('abcdefgh'):
    p = ''.join(p)
    day = Day21(p)
    day.scramble('input_21.txt')
    if ''.join(day.data) == 'fbgdceah':
        print(p)
        break
