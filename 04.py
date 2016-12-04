#!/usr/bin/python

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
import re
import string

INPUT = 'input_04.txt'
PATTERN = re.compile('([a-z-]+)-(\d+)\[([a-z]+)\]')

d_az = string.ascii_lowercase + string.ascii_lowercase
l_az = len(string.ascii_lowercase)

data = open(INPUT, 'r').readlines()
data = [PATTERN.match(x).groups() for x in data]


def translate_name(name, number):
    shift = int(number) % l_az  # maximum rotation is 25 chars
    # table = { 1: 'a', 2: 'b', }
    # where index is the ascii code of the character
    table = dict(
        zip(
            map(ord, string.ascii_lowercase),
            d_az[shift:shift + l_az]
        )
    )
    return name.translate(table)


room = 0
northpole = None

for name, number, checksum in data:
    logging.debug('name: %s, number: %s, checksum: %s', name, number, checksum)
    c = sorted([(-name.count(x), x) for x in string.ascii_lowercase])
    for (count, l1), l2 in zip(c[:len(checksum)], checksum):
        if l1 != l2:
            break
    else:
        logging.info('valid room %s, %s, %s', translate_name(name, number), number, checksum)
        room += int(number)
        if translate_name(name, number) == 'northpole-object-storage':
            northpole = number

logging.info('sum of room ids: %s', room)
logging.info('northpole: %s', northpole)
