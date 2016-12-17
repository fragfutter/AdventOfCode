#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

LENGTH = 272
LENGTH = 35651584
START = '00101000101111010'


def reverse1(data):
    length = len(bin(data)) - 2
    result = 0
    mask = 1
    for i in range(length):
        if data & mask:
            result += 1
        result = result << 1
        mask = mask << 1
    return result


def reverse(data):
    result = data.copy()
    result.reverse()
    return result


def flip(data):
    return map(lambda x: not x, data)


def dragon1(data):
    b = reverse(data)
    b = flip(b)
    data.append(False)
    data.extend(b)


def dragon(data):
    b = list(map(lambda x: not x, data))
    b.reverse()
    data.append(False)
    data.extend(b)


def checksum(data):
    result = []
    i = iter(data)
    for x, y in zip(i, i):
        result.append(x == y)
    return result


def dump(data):
    return ''.join(['1' if i else '0' for i in data])


def convert(data):
    return [True if i == '1' else False for i in data]

a = convert(START)


while len(a) < LENGTH:
    print(len(a))
    dragon(a)

c = a[:LENGTH]
while len(c) % 2 != 1:
    c = checksum(c)

logging.info('result: %s', dump(c))
