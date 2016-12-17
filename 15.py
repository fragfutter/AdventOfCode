#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')

# total positions, current position)
disks = [(5, 4), (2, 1)]
disks = [(7, 0), (13, 0), (3, 2), (5, 2), (17, 0), (19, 7)]
disks = [(7, 0), (13, 0), (3, 2), (5, 2), (17, 0), (19, 7), (11, 0)]
time = 0

while True:
    time += 1
    for index, (mod, current) in enumerate(disks):
        result = (current + time + index) % mod
        if result != 0:
            break
    else:
        print(time - 1)
        break
