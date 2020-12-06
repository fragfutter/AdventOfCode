#!/usr/bin/pypy3

from advent import Advent
import re

"""
"""

def minmax(value, min_, max_):
    v = int(value)
    return v >= min_ and v <= max_


class Day(Advent):
    def prepare(self):
        result = []
        passport = {}
        for line in self.data.split('\n'):
            line = line.strip()
            # empty line, flush and start passport
            if not line:
                result.append(passport)
                passport = {}
                continue
            for field in line.split(' '):
                key, value = field.split(':')
                # both tasks ignore cid
                if key == 'cid':
                    continue
                passport[key] = value
        result.append(passport)
        self.data = result

    def solve1(self):
        result = 0
        # drop all invalid passports, not needed for part 2
        self.data = list(filter(lambda x: len(x) == 7, self.data))
        return len(self.data)

    def solve2(self):
        result = 0
        for passport in self.data:
            # now validate each field
            if not minmax(passport['byr'], 1920, 2002):
                continue
            if not minmax(passport['iyr'], 2010, 2020):
                continue
            if not minmax(passport['eyr'], 2020, 2030):
                continue
            hgt = passport['hgt']
            if hgt.endswith('cm'):
                if not minmax(hgt[:-2], 150, 193):
                    continue
            elif hgt.endswith('in'):
                if not minmax(hgt[:-2], 59, 76):
                    continue
            else:
                continue  # either cm or in!
            if not re.match(r'^#[0-9a-f]{6}$', passport['hcl']):
                continue
            if not passport['ecl'] in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
                continue
            if not re.match(r'^\d{9}$', passport['pid']):
                continue
            # optional cid
            result += 1
        return result
        pass


Day.main()
