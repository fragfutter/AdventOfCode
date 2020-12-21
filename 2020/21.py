#!/usr/bin/pypy3

from advent import Advent
import re
from collections import deque

"""
"""

class Day(Advent):
    def prepare(self):
        result = []
        pat = re.compile(r'(.*) \(contains (.*)\)')
        all_ingredients = set()
        all_allergenes = set()
        for line in self.data.split('\n'):
            line = line.strip()
            match = pat.match(line)
            ingredients = set(match.group(1).split(' '))
            allergenes = set(match.group(2).split(', '))
            result.append([ingredients, allergenes])
            all_ingredients.update(ingredients)
            all_allergenes.update(allergenes)
        self.data = result
        self.all_ingredients = all_ingredients
        self.all_allergenes = all_allergenes

    def run(self):
        risk = {}  # allergene -> possible in ingredients
        # start: allergene can be in any of the ingredients
        for allergene in self.all_allergenes:
            risk[allergene] = self.all_ingredients
        # loop over recipies
        for ingredients, allergenes in self.data:
            # allergene is listed on the right
            # so one of the ingredients on the left MUST be it
            # if it is not listed on the right, there still may be
            # the ingredient on the left, but we don't reduce the set
            for allergene in allergenes:
                risk[allergene] = risk[allergene].intersection(ingredients)
        # build a list off ingredients still candidate for allergene
        possible_has_allergene = set()
        for candidates in risk.values():
            possible_has_allergene.update(candidates)
        save_ingredients = set(self.all_ingredients)
        save_ingredients.difference_update(possible_has_allergene)
        # count ingredients
        part1 = 0
        for ingredients, _ in self.data:
            part1 += len(save_ingredients.intersection(ingredients))
        self.part1 = part1
        ### part2
        known = {}
        work = deque([[a, list(i)] for a, i in risk.items()])
        while work:
            allergene, candidates = work.popleft()
            for i in known.values():
                if i in candidates:
                    candidates.remove(i)
            if len(candidates) == 1:
                known[allergene] = candidates[0]
            else:
                work.append([allergene, candidates])
        part2 = [known[a] for a in sorted(known)]
        self.part2 = ','.join(part2)

    def solve1(self):
        self.run()
        return self.part1

    def solve2(self):
        return self.part2


Day.main()
