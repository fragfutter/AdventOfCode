#!/usr/bin/pypy3

from advent import Advent
import re
from collections import deque

"""
"""

class Day(Advent):
    def prepare(self):
        rules = deque()
        messages = []
        for line in self.data.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line[0] in ('a', 'b'):
                messages.append(line)
                continue
            number, rule = line.split(': ')
            if '|' in rule:
                rule = '(?: %s )' % rule
            rules.append((number, rule))
        self.messages = messages
        self.rules = rules

    def rule_zero(self, rules):
        #  merge to one regexp
        resolved = {}
        while rules:
            number, rule = rules.popleft()
            result = []
            for token in rule.split(' '):
                if token in ('(?:', ')', '|', ' ', ')+', '){}'):
                    result.append(token)
                elif token[0] == '"':
                    result.append(token[1])
                elif token in resolved:
                    result.append(resolved[token])
                else:
                    # unresolved
                    rules.append((number, rule))
                    break
            else:
                # all tokens resolved
                resolved[number] = ' '.join(result)
        # make patterns
        return resolved['0']

    def solve1(self):
        count = 0
        zero = self.rule_zero(deque(self.rules))
        zero = re.compile('^%s$' % zero, re.VERBOSE)
        for message in self.messages:
            if zero.match(message):
                print(message)
                count += 1
        return count

    def solve2(self):
        rules = deque()
        for number, rule in self.rules:
            if number == '8':
                rule = '(?: 42 )+'
            if number == '11':
                rule = '(?: 42 ){} (?: 31 ){}'
            rules.append((number, rule))
        pattern = '^%s$' % self.rule_zero(rules)
        print(pattern)
        pat_one = re.compile(pattern.replace('{}', '+'), re.VERBOSE)
        # then test if identical lenghts
        pat_len = []
        for i in range(1, 20):
            pat_len.append(
                re.compile(pattern.replace('{}', '{%s}' % i), re.VERBOSE)
            )
        count = 0
        for message in self.messages:
            # first test with arbitary lengths
            if not pat_one.match(message):
                continue
            # now verify equal lengths
            for pat in pat_len:
                if pat.match(message):
                    break
            else:
                continue  # pat_len did not match
            print(message)
            count += 1
        return count


Day.main()
