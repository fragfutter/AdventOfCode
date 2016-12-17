#!/usr/bin/python

import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
import re

INPUT = 'input_07.txt'
# match a character, if the next character is not the same
# match a character, match same character again
# match first character
abba = r'([a-z])(?!\1)([a-z])\2\1'
# match opening [
# any number of characters
# abba
# any number of characters
# closing ]
HYPERNET = re.compile(r'\[[a-z]*' + abba + r'[a-z]*\]')
# abba itself
ABBA = re.compile(abba)

SSL = re.compile(
    r"""
        ([a-z])(?!\1)([a-z])\1  # ABA
        [^@]*                   # anything but an @
        @
        [^@]*                   # anything but an @
        \2\1\2                  # BAB
    """, re.VERBOSE)

data = open(INPUT, 'r').readlines()

result = 0
for line in data:
    if ABBA.search(line):
        logging.debug('ABBA in line %s', line)
        if HYPERNET.search(line):
            logging.debug('HYPERNET in line %s', line)
        else:
            logging.debug('TLS for ip %s', line)
            result += 1
logging.info(result)


# TWO
result = 0
for line in data:
    # a line may have multiple hyper sections
    # n1 [h1] n2 [h2] n3
    # make it a string "n1 n2 n3 @ h1 h2"
    parts = re.split(r'\[([^\]]+)\]', line)  # n1, h1, n2, h2, n3, ...
    # take every uneven token and join them with a space
    # add an "@"
    # take every even token and join them with a space
    line = ' '.join(parts[::2]) + '@' + ' '.join(parts[1::2])
    if SSL.search(line):
        result += 1
logging.info(result)
