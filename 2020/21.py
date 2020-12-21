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
        # build a risk list, used in part1 and part2
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
        self.risk = risk

    def solve1(self):
        # take all ingredients
        save_ingredients = set(self.all_ingredients)
        # remove all possible allergene containing ingredients
        for candidates in self.risk.values():
            save_ingredients.difference_update(candidates)
        # count ingredients
        result = 0
        for ingredients, _ in self.data:
            result += len(save_ingredients.intersection(ingredients))
        return result

    def solve2(self):
        known = {}  # allergene -> ingredient  (1:1 mapping)
        work = deque([[a, list(i)] for a, i in self.risk.items()])
        while work:
            allergene, candidates = work.popleft()
            # remove all ingredients we already know
            for i in known.values():
                if i in candidates:
                    candidates.remove(i)
            if len(candidates) == 1:
                # if only one ingredient left it is the allergene
                known[allergene] = candidates[0]
            else:
                # otherwise we need to check again later
                work.append([allergene, candidates])
        # sorted by allergenes (keys)
        result = [known[a] for a in sorted(known)]
        return ','.join(result)


Day.main()
