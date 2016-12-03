#!/usr/bin/python

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
import numpy

INPUT = 'input_01.txt'

data = map(lambda x: x.strip(), open(INPUT, 'r').read().split(','))

direction = numpy.matrix([[0], [1]])
position = numpy.matrix([[0], [0]])
turn_r = numpy.matrix([[0, 1], [-1, 0]])
turn_l = numpy.matrix([[0, -1], [1, 0]])

locations = [position, ]
found = False

for t in data:
    logging.debug('step %s', t)
    if t[0] == 'R':
        direction = turn_r * direction
    else:
        direction = turn_l * direction
    for i in range(int(t[1:])):
        # we need to walk each step for part2
        position = position + direction
        for history in locations:
            if not found and numpy.all(history == position):
                found = True
                logging.info('location: %s = %s', position, sum(map(abs, position)))
        locations.append(position)

logging.info('end positions: %s = %s', position, sum(map(abs, position)))
