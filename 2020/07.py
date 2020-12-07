#!/usr/bin/pypy3

from advent import Advent
import re
"""
"""

class Day(Advent):
    MY_BAG = 'shiny gold'
    def prepare(self):
        result = {}
        pat_start = re.compile(r'(.*?) bags contain (.*)')
        pat_target = re.compile(r'(?:\s*(\d+) (.*?) bag)')
        for line in self.data.split('\n'):
            line = line.strip()
            start, rest = pat_start.match(line).groups()
            targets = [(int(count), bag) for count, bag in pat_target.findall(rest)]
            assert(start not in result)
            result[start] = targets
        self.data = result
        # build a reverse graph
        rev = {}
        for start, targets in self.data.items():
            for _, target in targets:
                if target in rev:
                    if start not in rev[target]:
                        rev[target].append(start)
                else:
                    rev[target] = [start]
        self.rev = rev

    def solve1(self):
        result = []
        queue = [self.MY_BAG]
        while queue:
            bag = queue.pop(0)
            if bag in result:
                continue
            result.append(bag)
            try:
                owners = self.rev[bag]
            except KeyError:
                continue
            queue.extend(owners)
        result.remove(self.MY_BAG)
        return len(result)

    def solve2(self):
        bagcount = {}  # name -> number of bags inside
        queue = list(self.data.keys())  # all bags
        while queue:
            # iterate over a copy so we can modify it
            for bag in queue[:]:
                # check if we know all bags that must be inside
                try:
                    value = 0
                    for count, contained in self.data[bag]:
                        value += count + count * bagcount[contained]
                    bagcount[bag] = value
                    queue.remove(bag)
                except KeyError:
                    # one bag was unknown, check this later
                    pass
        return bagcount[self.MY_BAG]

Day.main()
