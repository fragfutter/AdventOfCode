#!/usr/bin/python

import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
import hashlib
import re


SALT = 'zpqevtbw'
PATTERN3 = re.compile(r'(.)(?=\1{2})')
stash = {}


class Md5(object):
    def __init__(self, salt):
        self.salt = salt
        self.cache = {}

    def get(self, index):
        try:
            return self.cache[index]
        except KeyError:
            result = self.md5(index)
            self.cache[index] = result
            return result

    def md5(self, index):
        result = '%s%d' % (self.salt, index)
        result = hashlib.md5(result.encode('ascii'))
        for i in range(2016):
            result = hashlib.md5(result.digest())
        return result.hexdigest()


index = 0

m = Md5(SALT)
pad = {}

while len(pad) < 64:
    candidate = m.get(index)
    match = PATTERN3.search(candidate)
    if match:
        # logging.debug('testing %s, at index %d, triple %s', candidate, index, match.group(0))
        seven = match.group(0) * 5
        for i in range(1000):
            if seven in m.get(index + i + 1):
                pad[index] = candidate
                logging.debug('found %3d %s', index, candidate)
                logging.debug('total %d', len(pad))
                break
    index += 1

logging.info(max(pad.keys()))
