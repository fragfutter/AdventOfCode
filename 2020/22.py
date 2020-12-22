#!/usr/bin/pypy3

from advent import Advent
from collections import deque
import logging

"""
"""


class Day(Advent):
    def prepare(self):
        result = []
        stack = None
        for line in self.data.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line.startswith('Player'):
                if stack:
                    result.append(stack)
                stack = deque()
                continue
            stack.append(int(line))
        result.append(stack)
        self.data = result

    def score(self, stack1, stack2):
        if stack1:
            stack = stack1
        else:
            stack = stack2
        score = 0
        stack.reverse()
        result = sum([i * j for i, j in enumerate(stack, start=1)])
        return result

    def solve1(self):
        stack1 = deque(self.data[0])
        stack2 = deque(self.data[1])
        turn = 0
        while stack1 and stack2:
            turn += 1
            a = stack1.popleft()
            b = stack2.popleft()
            if a > b:
                stack1.append(a)
                stack1.append(b)
            else:
                stack2.append(b)
                stack2.append(a)
        return self.score(stack1, stack2)

    def solve2(self):
        def play(stack1, stack2, game=1):
            seen = set()
            turn = 1
            while stack1 and stack2:
                logging.debug('-- Round %d (Game %d) --', turn, game)
                logging.debug('Player 1 deck: %s', stack1)
                logging.debug('Player 2 deck: %s', stack2)
                key = (tuple(stack1), tuple(stack2))
                if key in seen:
                    winner = 1
                    return winner
                seen.add(key)
                a = stack1.pop(0)
                b = stack2.pop(0)
                if len(stack1) >= a and len(stack2) >= b:
                    # recurse
                    winner = play(stack1[:a], stack2[:b], game + 1)
                else:
                    # not enough cards determine winner by larger card
                    if a > b:
                        winner = 1
                    else:
                        winner = 2
                assert(winner in (1, 2))
                if winner == 1:
                    stack1.append(a)
                    stack1.append(b)
                else:
                    stack2.append(b)
                    stack2.append(a)
                turn += 1
            # final winner is the stack still having cards
            if stack1:
                return 1
            else:
                return 2

        # part2 working with arbitary indices
        stack1 = list(self.data[0])
        stack2 = list(self.data[1])
        play(stack1, stack2)
        return self.score(stack1, stack2)



logging.basicConfig(level=logging.INFO)
Day.main()
