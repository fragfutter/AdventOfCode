#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
import re
# import sys
# sys.setrecursionlimit(100000)

INPUT = 'input_09.txt'
PATTERN = re.compile(r'(.*?)\((\d+)x(\d+)\)(.*)')
data = open(INPUT, 'r').read().strip()
# data = '(27x12)(20x12)(13x14)(7x10)(1x12)A'
# data = 'X(8x2)(3x3)ABCY'


def decompress(data):
    """returns length of decompressed data"""
    if '(' not in data:
        return len(data)
    start = data.find('(')  # opening (
    data = data[start + 1:]  # count and remove anything before (
    result = start
    stop = data.find(')')  # closing )
    length, repeat = map(int, data[0:stop].split('x'))
    data = data[stop + 1:]
    # assuming no overlap in repeats
    result += decompress(data[:length] * repeat)
    result += decompress(data[length:])
    return result

#result = decompress(data)
#logging.info('result: %s', result)


# weighted list
weight = [1] * len(data)
result = 0
i = 0
while i < len(data):
    if data[i] == '(':
        stop = data.find(')', i)
        length, repeat = map(int, data[i + 1:stop].split('x'))
        i = stop + 1  # first char after closing )
        # increase weight of everything for length
        for j in range(length):
            weight[i + j] *= repeat
    else:
        result += weight[i]
        i += 1

logging.info('result: %s', result)
