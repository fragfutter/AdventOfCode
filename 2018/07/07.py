#!/usr/bin/python

import logging
from copy import deepcopy

from advent import Advent

"""
--- Day 7: The Sum of Its Parts ---
You find yourself standing on a snow-covered coastline; apparently, you landed
a little off course. The region is too hilly to see the North Pole from here,
but you do spot some Elves that seem to be trying to unpack something that
washed ashore. It's quite cold out, so you decide to risk creating a paradox by
asking them for directions.

"Oh, are you the search party?" Somehow, you can understand whatever Elves from
the year 1018 speak; you assume it's Ancient Nordic Elvish. Could the device on
your wrist also be a translator? "Those clothes don't look very warm; take
this." They hand you a heavy coat.

"We do need to find our way back to the North Pole, but we have higher
priorities at the moment. You see, believe it or not, this box contains
something that will solve all of Santa's transportation problems - at least,
that's what it looks like from the pictures in the instructions." It doesn't
seem like they can read whatever language it's in, but you can: "Sleigh kit.
Some assembly required."

"'Sleigh'? What a wonderful name! You must help us assemble this 'sleigh' at
once!" They start excitedly pulling more parts out of the box.

The instructions specify a series of steps and requirements about which steps
must be finished before others can begin (your puzzle input). Each step is
designated by a single letter. For example, suppose you have the following
instructions:

  Step C must be finished before step A can begin.
  Step C must be finished before step F can begin.
  Step A must be finished before step B can begin.
  Step A must be finished before step D can begin.
  Step B must be finished before step E can begin.
  Step D must be finished before step E can begin.
  Step F must be finished before step E can begin.

Visually, these requirements look like this:


    -->A--->B--
   /    \      \
  C      -->D----->E
   \           /
    ---->F-----

Your first goal is to determine the order in which the steps should be
completed. If more than one step is ready, choose the step which is first
alphabetically. In this example, the steps would be completed as follows:

  - Only C is available, and so it is done first.
  - Next, both A and F are available. A is first alphabetically, so it is done
    next.
  - Then, even though F was available earlier, steps B and D are now also
    available, and B is the first alphabetically of the three.
  - After that, only D and F are available. E is not available because only
    some of its prerequisites are complete. Therefore, D is completed next.
  - F is the only choice, so it is done next.
  - Finally, E is completed.

So, in this example, the correct order is CABDFE.

In what order should the steps in your instructions be completed?

"""
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('07')


class Worker(object):
    basetime = 60

    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.task = None
        self.timer = 0

    def pick(self):
        """take a task"""
        candidates = [k for k, v in self.data.items() if not v]
        try:
            c = sorted(candidates)[0]
        except IndexError:
            log.debug("worker %s is idle", self.name)
            return  # nothing available, stay idle
        self.task = c
        log.debug("worker %s takes %s", self.name, self.task)
        # remove it (we are working on it)
        del(self.data[c])
        self.timer = self.basetime + ord(c) - ord('A') + 1

    def complete(self):
        log.debug("worker %s completed %s", self.name, self.task)
        for key, value in self.data.items():
            try:
                value.remove(self.task)
            except ValueError:
                pass
        self.task = None

    def tick(self):
        if self.timer > 0:
            self.timer -= 1

    def idle(self):
        return self.timer == 0


class Day(Advent):
    lines = True

    @classmethod
    def conversion(cls, line):
        data = line.split(' ')
        return (data[1], data[7])

    def prepare(self):
        super(Day, self).prepare()
        # determine all nodes
        nodes = [x[0] for x in self.data]
        nodes.extend([x[1] for x in self.data])
        self.nodes = set(nodes)
        edges = {}
        for node in self.nodes:
            edges[node] = []
        for a, b in self.data:
            edges[b].append(a)  # b requires a
        self.edges = edges

    def run(self, count):
        edges = deepcopy(self.edges)
        workers = []
        for i in range(count):
            workers.append(Worker(i, edges))
        i = 0
        # break if all workers become idle
        while edges or [worker for worker in workers if worker.task]:
            complete = []
            # complete
            for worker in workers:
                if worker.task and worker.timer == 0:
                    complete.append(worker.task)
                    worker.complete()
            # pick
            for worker in workers:
                if worker.task is None and worker.timer == 0:
                    worker.pick()
            # tick everyone
            for worker in workers:
                worker.tick()
            # in case multiple tasks complete in the same second
            # yield completed tasks in alphabetical order
            for task in sorted(complete):
                yield task
            i += 1
        yield i - 1

    def solve1(self):
        return ''.join(
            list(self.run(1))[:-1]
        )

    def solve2(self):
        return list(self.run(5))[-1]


Day.main()
