#!/usr/bin/pypy3

from advent import Advent
from collections import defaultdict

"""
--- Day 14: Space Stoichiometry ---
As you approach the rings of Saturn, your ship's low fuel indicator turns on.
There isn't any fuel here, but the rings have plenty of raw material. Perhaps
your ship's Inter-Stellar Refinery Union brand nanofactory can turn these raw
materials into fuel.

You ask the nanofactory to produce a list of the reactions it can perform that
are relevant to this process (your puzzle input). Every reaction turns some
quantities of specific input chemicals into some quantity of an output chemical.
Almost every chemical is produced by exactly one reaction; the only exception,
ORE, is the raw material input to the entire process and is not produced by a
reaction.

You just need to know how much ORE you'll need to collect before you can produce
one unit of FUEL.

Each reaction gives specific quantities for its inputs and output; reactions
cannot be partially run, so only whole integer multiples of these quantities can
be used. (It's okay to have leftover chemicals when you're done, though.) For
example, the reaction 1 A, 2 B, 3 C => 2 D means that exactly 2 units of
chemical D can be produced by consuming exactly 1 A, 2 B and 3 C. You can run
the full reaction as many times as necessary; for example, you could produce 10
D by consuming 5 A, 10 B, and 15 C.

Suppose your nanofactory produces the following list of reactions:

10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL

The first two reactions use only ORE as inputs; they indicate that you can
produce as much of chemical A as you want (in increments of 10 units, each 10
costing 10 ORE) and as much of chemical B as you want (each costing 1 ORE). To
produce 1 FUEL, a total of 31 ORE is required: 1 ORE to produce 1 B, then 30
more ORE to produce the 7 + 7 + 7 + 7 = 28 A (with 2 extra A wasted) required in
the reactions to convert the B into C, C into D, D into E, and finally E into
FUEL. (30 A is produced because its reaction requires that it is created in
increments of 10.) """

class Day(Advent):
    lines = True

    def prepare(self):
        def token(data):
            amount, value = data.split(' ')
            return int(amount), value

        super(Day, self).prepare()
        result = []
        for line in self.data:
            record = []
            i, o = line.split(' => ')
            record.append(token(o))
            for si in i.split(', '):
                record.append(token(si))
            result.append(record)
        self.data = result

    def digraph(self):
        print('digraph foo {')
        for record in self.data:
            o = record[0][1]
            for i in record[1:]:
                print('%s -> %s;' % (i[1], o))
        print('}')

    def cookbook(self, ingredient):
        for recipe in self.data:
            if recipe[0][1] == ingredient:
                return recipe
        raise Exception('unknown ingredient %s' % ingredient)

    def stir(self, pantry, requests):
        """process one request, update pantry, return consumed ore"""
        wanted, ingredient = requests.pop(0)
        # ore falls from heaven
        if ingredient == 'ORE':
            return wanted
        if pantry[ingredient] >= wanted:
            # consume pantry
            pantry[ingredient] -= wanted
            return 0
        # not enough in the pantry
        # consume what is there
        wanted -= pantry[ingredient]
        pantry[ingredient] = 0
        # produce what is missing
        recipe = self.cookbook(ingredient)
        scale = (wanted - 1) // recipe[0][0] + 1  # scale up
        pantry[ingredient] = recipe[0][0] * scale - wanted  # store leftover
        # add required stuff
        for source_amount, source_ingredient in recipe[1:]:
            requests.append((source_amount * scale, source_ingredient))
        return 0

    def solve1(self):
        ore = 0
        requests = [(1, 'FUEL')]
        pantry = defaultdict(lambda: 0)
        while requests:
            ore += self.stir(pantry, requests)
        self.minimum_ore = ore
        return ore


    def solve2(self):
        fuel = 0
        ore = 1000000000000
        requests = []
        pantry = defaultdict(lambda: 0)
        while ore > self.minimum_ore:
            if not requests:
                # speed up, try to consume half the ore left
                requests.append((ore // (self.minimum_ore * 2) + 1, 'FUEL'))
            # take a peak if we produce fuel and remember it
            if requests[0][1] == 'FUEL':
                fuel += requests[0][0]
            ore -= self.stir(pantry, requests)
        return fuel


Day.main()
