#!/usr/bin/pypy3

from advent import Advent
import re
from collections import defaultdict

"""
"""

class Day(Advent):
    def prepare(self):
        pat_field = re.compile(r'^(.*): (\d+)-(\d+) or (\d+)-(\d+)$')
        pat_ticket = re.compile(r'^[0-9,]+$')
        fields = {}
        my_ticket = None
        tickets = []
        for line in self.data.split('\n'):
            line = line.strip()
            if pat_field.match(line):
                name, a, b, c, d = pat_field.match(line).groups()
                fields[name] = \
                    list(range(int(a), int(b)+1)) + \
                    list(range(int(c), int(d)+1))
            elif pat_ticket.match(line):
                values = [int(x) for x in line.split(',')]
                if not my_ticket:
                    my_ticket = values
                else:
                    tickets.append(values)
        self.fields = fields
        self.my_ticket = my_ticket
        self.tickets = tickets

    def solve1(self):
        valid_values = []
        for values in self.fields.values():
            valid_values.extend(values)
        result = 0
        for ticket in self.tickets:
            for v in ticket:
                if v not in valid_values:
                    result += v
        return result

    def solve2(self):
        def validate(fieldname, values):
            for v in values:
                if v not in self.fields[fieldname]:
                    return False
            return True


        # create dictionary where each column holds all valid values
        flipped = defaultdict(list)
        valid_values = []
        for values in self.fields.values():
            valid_values.extend(values)
        for ticket in self.tickets:
            for v in ticket:
                if v not in valid_values:
                    break
            else:
                # ticket is valid
                for i, v in enumerate(ticket):
                    flipped[i].append(v)
        # for each column determine the possible fieldnames
        options = defaultdict(list)
        for i, values in flipped.items():
            for name in self.fields.keys():
                if validate(name, values):
                    options[i].append(name)
        # assume there is a unique solution
        # for one column there is only one option.
        # remove that option from all remaining columns
        # etc.
        translation = {}  # fieldname to column
        for idx, row in sorted(options.items(),key=lambda x: len(x[1])):
            for name in row:
                if name not in translation.keys():
                    translation[name] = idx
                    break
        result = 1
        for name, idx in translation.items():
            if name.startswith('departure'):
                result *= self.my_ticket[idx]
        return result


Day.main()
