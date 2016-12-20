#!/usr/bin/python

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

data = open('input_20.txt', 'r').readlines()
data = [tuple(map(int, x.split('-'))) for x in data]
data.sort()

# merge all ranges
i = 0
while True:
    a = data[i]
    try:
        b = data[i + 1]
    except IndexError:
        break
    logging.debug('merging %s with %s', a, b)
    if (a[1] + 1) >= b[0]:
        if b[1] > a[1]:
            # the end of range b is higher then our current end
            data[i] = (a[0], b[1])
        else:
            # we already end past range b, keep it
            # no need to reassign
            # data[i] = (a[0], a[1])
            pass
        del data[i + 1]  # remove the merged range
    else:
        i += 1

logging.debug(data)

assert(data[0][0] == 0)  # otherwise it is 0
logging.info('part 1: %d', data[0][1] + 1)

result = 2 ** 32
for x, y in data:
    result = result - y + x - 1

logging.info('part 2: %d', result)
