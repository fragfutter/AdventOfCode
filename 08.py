#!/usr/bin/python

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
import numpy

INPUT = 'input_08.txt'
data = open(INPUT, 'r').readlines()

display = numpy.array([[0] * 50] * 6)


def dump():
    for row in display:
        print(''.join(['.' if x == 0 else '#' for x in row]))


def lights():
    print(sum(sum(display)))


def rect(x, y):
    for row in range(y):
        for col in range(x):
            display[row, col] = 1


def rotate(xy, n, column=False):
    global display
    if column:
        display = numpy.rot90(display)
        display = numpy.rot90(display)
        display = numpy.rot90(display)
        display[xy] = numpy.roll(display[xy], len(display[xy]) - n)
        display = numpy.rot90(display)
    else:
        display[xy] = numpy.roll(display[xy], n)


for line in data:
    a = line.split(' ')
    if a[0] == 'rect':
        x, y = map(int, a[1].split('x'))
        rect(x, y)
    else:
        column = a[1] == 'column'
        xy = int(a[2].split('=')[1])
        n = int(a[4])
        rotate(xy, n, column)
dump()
lights()
