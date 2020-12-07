#!/usr/bin/pypy3

from advent import Advent
import re
from collections import deque  # we use lists as fifo, this is faster
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
        # build a reverse graph, used in part1
        rev = {}
        for start, targets in self.data.items():
            for _, target in targets:  # not interested in count
                if target in rev:
                    if start not in rev[target]:
                        rev[target].append(start)
                else:
                    rev[target] = [start]
        self.rev = rev

    def solve1(self):
        result = []
        queue = deque([self.MY_BAG])
        while queue:
            bag = queue.popleft()
            if bag in result:
                continue
            result.append(bag)
            try:
                owners = self.rev[bag]
            except KeyError:
                continue
            queue.extend(owners)
        result.remove(self.MY_BAG)  # our bag is not allowed to travel by itself
        return len(result)

    def solve2(self):
        """idea is to find all bags for which we can know the counts
        avoiding to recalculate the same values over and over,
        avoiding to hit a recursion limit.
        In the end we know the count for all bags, as this is Adventofcode
        i assume that we need to know it anyway and there are no seperate
        bag-loops"""
        bagcount = {}  # name -> number of bags inside
        queue = deque(self.data.keys())  # all bags
        while queue:
            bag = queue.popleft()  # take a bag
            # check if we know all bags that must be inside
            try:
                value = 0
                for count, contained in self.data[bag]:
                    value += count + count * bagcount[contained]
                bagcount[bag] = value
            except KeyError:
                # for one bag we did not know how many others it contained
                # add it back to the queue, we will check it later
                queue.append(bag)
        return bagcount[self.MY_BAG]

Day.main()
