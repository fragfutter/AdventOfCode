#!/usr/bin/python
import logging
from copy import deepcopy

from advent import Advent

"""
-- Day 15: Beverage Bandits ---
Having perfected their hot chocolate, the Elves have a new problem: the Goblins
that live in these caves will do anything to steal it. Looks like they're here
for a fight.

You scan the area, generating a map of the walls (#), open cavern (.), and
starting position of every Goblin (G) and Elf (E) (your puzzle input).

Combat proceeds in rounds; in each round, each unit that is still alive takes a
turn, resolving all of its actions before the next unit's turn begins. On each
unit's turn, it tries to move into range of an enemy (if it isn't already)
and then attack (if it is in range).

All units are very disciplined and always follow very strict combat rules. Units
never move or attack diagonally, as doing so would be dishonorable. When
multiple choices are equally valid, ties are broken in reading order:

top-to-bottom, then left-to-right. For instance, the order in which units take
their turns within a round is the reading order of their starting positions in
that round, regardless of the type of unit or whether other units have moved
after the round started. For example:

                   would take their
  These units:   turns in this order:
    #######           #######
    #.G.E.#           #.1.2.#
    #E.G.E#           #3.4.5#
    #.G.E.#           #.6.7.#
    #######           #######

Each unit begins its turn by identifying all possible targets (enemy units). If
no targets remain, combat ends.

Then, the unit identifies all of the open squares (.) that are in range of each
target; these are the squares which are adjacent (immediately up, down, left, or
right) to any target and which aren't already occupied by a wall or
another unit. Alternatively, the unit might already be in range of a target. If
the unit is not already in range of a target, and there are no open squares
which are in range of a target, the unit ends its turn.

If the unit is already in range of a target, it does not move, but continues its
turn with an attack. Otherwise, since it is not in range of a target, it moves.

To move, the unit first considers the squares that are in range and determines
which of those squares it could reach in the fewest steps. A step is a single
movement to any adjacent (immediately up, down, left, or right) open (.)
square. Units cannot move into walls or other units. The unit does this while
considering the current positions of units and does not do any prediction about
where units will be later. If the unit cannot reach (find an open path to)
any of the squares that are in range, it ends its turn. If multiple squares are
in range and tied for being reachable in the fewest steps, the square which is
first in reading order is chosen. For example:

  Targets:      In range:     Reachable:    Nearest:      Chosen:
  #######       #######       #######       #######       #######
  #E..G.#       #E.?G?#       #E.@G.#       #E.!G.#       #E.+G.#
  #...#.#  -->  #.?.#?#  -->  #.@.#.#  -->  #.!.#.#  -->  #...#.#
  #.G.#G#       #?G?#G#       #@G@#G#       #!G.#G#       #.G.#G#
  #######       #######       #######       #######       #######

In the above scenario, the Elf has three targets (the three Goblins):

  - Each of the Goblins has open, adjacent squares which are in range (marked
  with a ? on the map).
  - Of those squares, four are reachable (marked @); the other two (on the
  right) would require moving through a wall or unit to reach.
  - Three of these reachable squares are nearest, requiring the fewest steps
  (only 2) to reach (marked !).
  - Of those, the square which is first in reading order is chosen (+).

The unit then takes a single step toward the chosen square along the shortest
path to that square. If multiple steps would put the unit equally closer to its
destination, the unit chooses the step which is first in reading order. (This
requires knowing when there is more than one shortest path so that you can
consider the first step of each such path.) For example:

  In range:     Nearest:      Chosen:       Distance:     Step:
  #######       #######       #######       #######       #######
  #.E...#       #.E...#       #.E...#       #4E212#       #..E..#
  #...?.#  -->  #...!.#  -->  #...+.#  -->  #32101#  -->  #.....#
  #..?G?#       #..!G.#       #...G.#       #432G2#       #...G.#
  #######       #######       #######       #######       #######

The Elf sees three squares in range of a target (?), two of which are nearest
(!), and so the first in reading order is chosen (+). Under "Distance", each
open square is marked with its distance from the destination square; the two
squares to which the Elf could move on this turn (down and to the right) are
both equally good moves and would leave the Elf 2 steps from being in range of
the Goblin. Because the step which is first in reading order is chosen, the Elf
moves right one square.

Here's a larger example of movement:

  Initially:
  #########
  #G..G..G#
  #.......#
  #.......#
  #G..E..G#
  #.......#
  #.......#
  #G..G..G#
  #########

  After 1 round:
  #########
  #.G...G.#
  #...G...#
  #...E..G#
  #.G.....#
  #.......#
  #G..G..G#
  #.......#
  #########

  After 2 rounds:
  #########
  #..G.G..#
  #...G...#
  #.G.E.G.#
  #.......#
  #G..G..G#
  #.......#
  #.......#
  #########

  After 3 rounds:
  #########
  #.......#
  #..GGG..#
  #..GEG..#
  #G..G...#
  #......G#
  #.......#
  #.......#
  #########

Once the Goblins and Elf reach the positions above, they all are either in range
of a target or cannot find any square in range of a target, and so none of the
units can move until a unit dies.

After moving (or if the unit began its turn in range of a target), the unit
attacks.

To attack, the unit first determines all of the targets that are in range of it
by being immediately adjacent to it.  If there are no such targets, the unit
ends its turn. Otherwise, the adjacent target with the fewest hit points is
selected; in a tie, the adjacent target with the fewest hit points which is
first in reading order is selected.

The unit deals damage equal to its attack power to the selected target, reducing
its hit points by that amount. If this reduces its hit points to 0 or fewer, the
selected target dies: its square becomes . and it takes no further turns.

Each unit, either Goblin or Elf, has 3 attack power and starts with 200 hit
points.

For example, suppose the only Elf is about to attack:

         HP:            HP:
  G....  9       G....  9
  ..G..  4       ..G..  4
  ..EG.  2  -->  ..E..
  ..G..  2       ..G..  2
  ...G.  1       ...G.  1

The "HP" column shows the hit points of the Goblin to the left in the
corresponding row. The Elf is in range of three targets: the Goblin above it
(with 4 hit points), the Goblin to its right (with 2 hit points), and the Goblin
below it (also with 2 hit points). Because three targets are in range, the ones
with the lowest hit points are selected: the two Goblins with 2 hit points each
(one to the right of the Elf and one below the Elf). Of those, the Goblin first
in reading order (the one to the right of the Elf) is selected. The selected
Goblin's hit points (2) are reduced by the Elf's attack power (3), reducing its
hit points to -1, killing it.

After attacking, the unit's turn ends. Regardless of how the unit's turn ends,
the next unit in the round takes its turn. If all units have taken turns in this
round, the round ends, and a new round begins.

The Elves look quite outnumbered. You need to determine the outcome of the
battle: the number of full rounds that were completed (not counting the round in
which combat ends) multiplied by the sum of the hit points of all remaining
units at the moment combat ends. (Combat only ends when a unit finds no targets
during its turn.)

Below is an entire sample combat. Next to each map, each row's units' hit points
are listed from left to right.

  Initially:
  #######
  #.G...#   G(200)
  #...EG#   E(200), G(200)
  #.#.#G#   G(200)
  #..G#E#   G(200), E(200)
  #.....#
  #######

  After 1 round:
  #######
  #..G..#   G(200)
  #...EG#   E(197), G(197)
  #.#G#G#   G(200), G(197)
  #...#E#   E(197)
  #.....#
  #######

  After 2 rounds:
  #######
  #...G.#   G(200)
  #..GEG#   G(200), E(188), G(194)
  #.#.#G#   G(194)
  #...#E#   E(194)
  #.....#
  #######

  Combat ensues; eventually, the top Elf dies:

  After 23 rounds:
  #######
  #...G.#   G(200)
  #..G.G#   G(200), G(131)
  #.#.#G#   G(131)
  #...#E#   E(131)
  #.....#
  #######

  After 24 rounds:
  #######
  #..G..#   G(200)
  #...G.#   G(131)
  #.#G#G#   G(200), G(128)
  #...#E#   E(128)
  #.....#
  #######

  After 25 rounds:
  #######
  #.G...#   G(200)
  #..G..#   G(131)
  #.#.#G#   G(125)
  #..G#E#   G(200), E(125)
  #.....#
  #######

  After 26 rounds:
  #######
  #G....#   G(200)
  #.G...#   G(131)
  #.#.#G#   G(122)
  #...#E#   E(122)
  #..G..#   G(200)
  #######

  After 27 rounds:
  #######
  #G....#   G(200)
  #.G...#   G(131)
  #.#.#G#   G(119)
  #...#E#   E(119)
  #...G.#   G(200)
  #######

  After 28 rounds:
  #######
  #G....#   G(200)
  #.G...#   G(131)
  #.#.#G#   G(116)
  #...#E#   E(113)
  #....G#   G(200)
  #######

  More combat ensues; eventually, the bottom Elf dies:

  After 47 rounds:
  #######
  #G....#   G(200)
  #.G...#   G(131)
  #.#.#G#   G(59)
  #...#.#
  #....G#   G(200)
  #######


Before the 48th round can finish, the top-left Goblin finds that there are no
targets remaining, and so combat ends.  So, the number of full rounds that were
completed is 47, and the sum of the hit points of all remaining units is
200+131+59+200 = 590. From these, the outcome of the battle is 47 * 590 = 27730.

  Here are a few example summarized combats:

  #######       #######
  #G..#E#       #...#E#   E(200)
  #E#E.E#       #E#...#   E(197)
  #G.##.#  -->  #.E##.#   E(185)
  #...#E#       #E..#E#   E(200), E(200)
  #...E.#       #.....#
  #######       #######

  Combat ends after 37 full rounds
  Elves win with 982 total hit points left
  Outcome: 37 * 982 = 36334
  #######       #######
  #E..EG#       #.E.E.#   E(164), E(197)
  #.#G.E#       #.#E..#   E(200)
  #E.##E#  -->  #E.##.#   E(98)
  #G..#.#       #.E.#.#   E(200)
  #..E#.#       #...#.#
  #######       #######

  Combat ends after 46 full rounds
  Elves win with 859 total hit points left
  Outcome: 46 * 859 = 39514
  #######       #######
  #E.G#.#       #G.G#.#   G(200), G(98)
  #.#G..#       #.#G..#   G(200)
  #G.#.G#  -->  #..#..#
  #G..#.#       #...#G#   G(95)
  #...E.#       #...G.#   G(200)
  #######       #######

  Combat ends after 35 full rounds
  Goblins win with 793 total hit points left
  Outcome: 35 * 793 = 27755
  #######       #######
  #.E...#       #.....#
  #.#..G#       #.#G..#   G(200)
  #.###.#  -->  #.###.#
  #E#G#G#       #.#.#.#
  #...#G#       #G.G#G#   G(98), G(38), G(200)
  #######       #######

  Combat ends after 54 full rounds
  Goblins win with 536 total hit points left
  Outcome: 54 * 536 = 28944
  #########       #########
  #G......#       #.G.....#   G(137)
  #.E.#...#       #G.G#...#   G(200), G(200)
  #..##..G#       #.G##...#   G(200)
  #...##..#  -->  #...##..#
  #...#...#       #.G.#...#   G(200)
  #.G...G.#       #.......#
  #.....G.#       #.......#
  #########       #########

Combat ends after 20 full rounds
Goblins win with 937 total hit points left
Outcome: 20 * 937 = 18740
What is the outcome of the combat described in your puzzle input?

--- Part Two ---
According to your calculations, the Elves are going to lose badly. Surely, you
won't mess up the timeline too much if you give them just a little advanced
technology, right?

You need to make sure the Elves not only win, but also suffer no losses: even
the death of a single Elf is unacceptable.

However, you can't go too far: larger changes will be more likely to permanently alter spacetime.

So, you need to find the outcome of the battle in which the Elves have the
lowest integer attack power (at least 4) that allows them to win without a
single death. The Goblins always have an attack power of 3.

In the first summarized example above, the lowest attack power the Elves need to
win without losses is 15:

#######       #######
#.G...#       #..E..#   E(158)
#...EG#       #...E.#   E(14)
#.#.#G#  -->  #.#.#.#
#..G#E#       #...#.#
#.....#       #.....#
#######       #######

Combat ends after 29 full rounds
Elves win with 172 total hit points left
Outcome: 29 * 172 = 4988
In the second example above, the Elves need only 4 attack power:

#######       #######
#E..EG#       #.E.E.#   E(200), E(23)
#.#G.E#       #.#E..#   E(200)
#E.##E#  -->  #E.##E#   E(125), E(200)
#G..#.#       #.E.#.#   E(200)
#..E#.#       #...#.#
#######       #######

Combat ends after 33 full rounds
Elves win with 948 total hit points left
Outcome: 33 * 948 = 31284
In the third example above, the Elves need 15 attack power:

#######       #######
#E.G#.#       #.E.#.#   E(8)
#.#G..#       #.#E..#   E(86)
#G.#.G#  -->  #..#..#
#G..#.#       #...#.#
#...E.#       #.....#
#######       #######

Combat ends after 37 full rounds
Elves win with 94 total hit points left
Outcome: 37 * 94 = 3478
In the fourth example above, the Elves need 12 attack power:

#######       #######
#.E...#       #...E.#   E(14)
#.#..G#       #.#..E#   E(152)
#.###.#  -->  #.###.#
#E#G#G#       #.#.#.#
#...#G#       #...#.#
#######       #######

Combat ends after 39 full rounds
Elves win with 166 total hit points left
Outcome: 39 * 166 = 6474
In the last example above, the lone Elf needs 34 attack power:

#########       #########
#G......#       #.......#
#.E.#...#       #.E.#...#   E(38)
#..##..G#       #..##...#
#...##..#  -->  #...##..#
#...#...#       #...#...#
#.G...G.#       #.......#
#.....G.#       #.......#
#########       #########

Combat ends after 30 full rounds
Elves win with 38 total hit points left
Outcome: 30 * 38 = 1140
After increasing the Elves' attack power until it is just barely enough for them
to win without any Elves dying, what is the outcome of the combat described in
your puzzle input?

"""

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


class NoMoreEnemies(Exception):
    pass


class DeadElve(Exception):
    pass


class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '<Pos %s,%s>' % (self.x, self.y)

    def __hash__(self):
        return hash(self.pos)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @property
    def pos(self):
        return (self.x, self.y)

    def neighbours(self):
        yield Position(self.x, self.y - 1)
        yield Position(self.x - 1, self.y)
        yield Position(self.x + 1, self.y)
        yield Position(self.x, self.y + 1)

    def neighbours_on_grid(self, grid):
        """all neighbour positions that are on the grid and empty"""
        for n in self.neighbours():
            if n not in grid:
                continue  # not part of the grid (wall or outside)
            if grid[n] is None:
                yield n

    def distance(self, other):
        """manhatten distance"""
        return abs(self.x - other.x) + abs(self.y - other.y)


class Unit(Position):
    def __init__(self, x, y, race):
        super(Unit, self).__init__(x, y)
        self.hp = 200
        self.power = 3
        self.race = race

    def __str__(self):
        return '<Unit %s at %s,%s>' % (self.race, self.x, self.y)

    def free(self):
        if self.race == '.':
            return True
        if self.hp <= 0:
            return True
        return False

    def is_enemy(self, other):
        test = (self.race, other.race)
        return test in (('E', 'G'), ('G', 'E'))

    def attack(self, grid):
        enemy = None
        for n in self.neighbours():
            # we rely on neighbours to yield in preferred attack order
            # N, W, E, S
            if n not in grid:
                continue
            if grid[n] is None:
                continue
            if grid[n].race == self.race:
                continue
            if enemy is None:
                enemy = grid[n]
            else:
                if grid[n].hp < enemy.hp:
                    enemy = grid[n]
        if enemy is None:
            log.debug('%s has no target in range', self)
            return
        log.debug('%s attacks %s', self, enemy)
        enemy.hp -= self.power
        if enemy.hp <= 0:
            log.debug('%s has been killed', enemy)
            grid[enemy] = None

    def search_enemy(self, grid):
        """search the closest reachable enemy"""
        log.debug('%s is searching for enemies', self)
        targets = []
        units = filter(None, grid.values())
        units = filter(lambda u: u.race != self.race, units)
        units = list(units)  # otherwise we have filter expression
        if not units:
            raise NoMoreEnemies()
        for unit in units:
            for pos in unit.neighbours():
                try:
                    node = grid[pos]
                except KeyError:
                    # a wall or outside
                    continue
                if node is None:
                    targets.append(pos)
                    continue
                if node.pos == self.pos:
                    targets.append(pos)
                    continue
        # remove duplicates
        targets = set(targets)
        distance = 0
        seen = set()  # nodes visited
        options = [self]
        while options:
            # check if any option is good
            for p in sorted(options, key=lambda n: (n.y, n.x)):
                seen.add(p)
                if p in targets:
                    log.debug('found enemy %s with distance %s', p, distance)
                    return p, distance
            # increment distance, add all new options
            distance += 1
            work = options[:]
            options = []
            for p in work:
                for n in p.neighbours_on_grid(grid):
                    if n in seen:
                        continue
                    if n in options:
                        continue
                    options.append(n)
        return None, None  # no enemy found

    def step(self, enemy, grid):
        """walk back from enemy to one of our neighbour fields
        our neighbour fields will be sorted in preferred order
        """
        seen = set()
        targets = list(self.neighbours_on_grid(grid))
        options = [enemy]
        while options:
            for p in sorted(options, key=lambda n: (n.y, n.x)):
                seen.add(p)
                if p in targets:
                    log.debug('%s moving to %s', self, p)
                    grid[self] = None  # leave field
                    self.x = p.x
                    self.y = p.y
                    grid[self] = self
                    return
            work = options[:]
            for p in work:
                for n in p.neighbours_on_grid(grid):
                    if n in seen:
                        continue
                    if n in options:
                        continue
                    options.append(n)


def print_grid(grid):
    print()
    max_x = max([p.x for p in grid]) + 1
    max_y = max([p.y for p in grid]) + 1
    for y in range(max_y):
        for x in range(max_x):
            try:
                node = grid[Position(x, y)]
            except KeyError:
                print('#', end='')  # noqa
                continue
            if node is None:
                print('.', end='')  # noqa
            else:
                print(node.race, end='')  # noqa
        print()


class Day(Advent):
    lines = True

    def prepare(self):
        super(Day, self).prepare()
        grid = {}
        for y, line in enumerate(self.data):
            for x, value in enumerate(line):
                if value == '#':  # do not note walls
                    continue
                p = Position(x, y)
                if value == '.':
                    grid[p] = None
                else:
                    grid[p] = Unit(x, y, value)
        self.grid = grid

    def units(self, grid):
        units = filter(None, grid.values())
        units = sorted(units, key=lambda n: (n.y, n.x))
        return units

    def battle(self, grid, raise_elve=False):
        """execute one round of the battle"""
        units = self.units(grid)
        for unit in units:
            if unit.hp <= 0:
                continue  # dead, killed this round
            enemy, distance = unit.search_enemy(grid)
            if enemy is None:
                continue
            if distance > 0:
                unit.step(enemy, grid)
            unit.attack(grid)
        if raise_elve:
            for unit in units:
                if unit.hp <= 0 and unit.race == 'E':
                    raise DeadElve()

    def hastings(self, grid, raise_elve=False):
        """execute a complete battle
        (or wait for an elve to die)"""
        result = 0
        while True:
            try:
                self.battle(grid, raise_elve=raise_elve)
            except NoMoreEnemies:
                return result
            result += 1

    def solve1(self):
        grid = deepcopy(self.grid)
        battleround = self.hastings(grid)
        hp = sum([u.hp for u in self.units(grid)])
        return hp * battleround

    def solve2(self):
        power = 4
        while True:
            grid = deepcopy(self.grid)
            # upgrade elves
            for unit in self.units(grid):
                if unit.race == 'E':
                    unit.power = power
            # fight
            try:
                battleround = self.hastings(grid, raise_elve=True)
            except DeadElve:
                power += 1
                continue
            break
        hp = sum([u.hp for u in self.units(grid)])
        return hp * battleround

Day.main()
