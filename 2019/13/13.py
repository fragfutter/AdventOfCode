#!/usr/bin/pypy3

import re
import logging
from threading import Thread
from queue import Queue
from advent import Advent
from advent.intcode import Intcode

"""
--- Day 13: Care Package ---
As you ponder the solitude of space and the ever-increasing three-hour roundtrip
for messages between you and Earth, you notice that the Space Mail Indicator
Light is blinking. To help keep you sane, the Elves have sent you a care
package.

It's a new game for the ship's arcade cabinet! Unfortunately, the arcade is all
the way on the other end of the ship. Surely, it won't be hard to build your own
- the care package even comes with schematics.

The arcade cabinet runs Intcode software like the game the Elves sent (your
puzzle input). It has a primitive screen capable of drawing square tiles on a
grid. The software draws tiles to the screen with output instructions: every
three output instructions specify the x position (distance from the left), y
position (distance from the top), and tile id. The tile id is interpreted as
follows:

- 0 is an empty tile. No game object appears in this tile.
- 1 is a wall tile. Walls are indestructible barriers.
- 2 is a block tile. Blocks can be broken by the ball.
- 3 is a horizontal paddle tile. The paddle is indestructible.
- 4 is a ball tile. The ball moves diagonally and bounces off objects.

For example, a sequence of output values like 1,2,3,6,5,4 would draw a
horizontal paddle tile (1 tile from the left and 2 tiles from the top) and a
ball tile (6 tiles from the left and 5 tiles from the top).

Start the game. How many block tiles are on the screen when the game exits?
"""

EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4
INPUT = 98
TERMINATE = 99

LEFT = -1
RIGHT = 1
NEUTRAL = 0

class Arcade(Thread):
    def __init__(self, input_, output, event):
        super(Arcade, self).__init__()
        self.input_ = input_
        self.output = output
        self.event = event
        self.grid = {}
        self.score = -1

    def has_blocks(self):
        return BLOCK in self.grid.values()

    def process(self, x, y, value):
        if x == -1 and y == 0:
            self.score = value
        else:
            self.grid[(x, y)] = value

    def get_position(self, item):
        for k, v in self.grid.items():
            if v == item:
                logging.debug('found %s at %s', item, k)
                return k
        return 0, 0

    def joystick(self):
        ball, _ = self.get_position(BALL)
        paddle, _ = self.get_position(PADDLE)
        if ball < paddle:
            move = LEFT
        elif ball > paddle:
            move = RIGHT
        else:
            move = NEUTRAL
        self.output.put(move)
        count_ = list(self.grid.values()).count(BLOCK)

    def run(self):
        while True:
            # wait for vm
            self.event.wait()
            # process everything the vm produced
            while not self.input_.empty():
                x = self.input_.get()
                if x == TERMINATE:
                    return
                y = self.input_.get()
                value = self.input_.get()
                self.process(x, y, value)
            # reset event
            self.event.clear()
            # check for termination
            if not self.has_blocks():
                break
            # generate joystick movement for the vm
            self.joystick()



class Day(Advent):
    matrix = True
    seperator = re.compile(',')
    conversion = int

    def prepare(self):
        super(Day, self).prepare()
        self.data = self.data[0]

    def run(self, data):
        input_ = Queue()
        output = Queue()
        pc = Intcode(data, input_, output)
        arc = Arcade(output, input_, pc.waiting_for_input)
        pc.start()
        arc.start()
        pc.join()
        output.put(TERMINATE)
        pc.waiting_for_input.set()  # process remaining output
        arc.join()
        return arc

    def solve1(self):
        arc = self.run(self.data)
        return list(arc.grid.values()).count(BLOCK)

    def solve2(self):
        data = self.data[:]
        data[0] = 2
        arc = self.run(data)
        return arc.score


Day.main()
