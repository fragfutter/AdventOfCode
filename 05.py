#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
import hashlib

INPUT = 'abbhdwsy'
TWO = True

i = 0
result = ''


if not TWO:
    while len(result) < 8:
        s = INPUT + str(i)
        h = hashlib.md5(s.encode()).hexdigest()
        if h[:5] == '00000':
            logging.debug('%d results in %s', i, h)
            result += h[5]
        i += 1

if TWO:
    result = ['_'] * 8
    while '_' in result:
        s = INPUT + str(i)
        h = hashlib.md5(s.encode()).hexdigest()
        i += 1
        if h[:5] != '00000':
            continue
        logging.debug('%d results in %s, %s', i, h, ''.join(result))
        try:
            j = int(h[5])
        except ValueError:
            logging.debug('not a number')
            continue
        if j > 7:
            logging.debug('too high')
            continue
        if result[j] != '_':
            logging.debug('already taken')
            continue
        logging.debug('assigning %s', h[6])
        result[j] = h[6]


logging.info(result)
