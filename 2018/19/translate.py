#!/usr/bin/python

data = open('input.txt', 'r').readlines()
data = [line.strip().split() for line in data]
data.pop(0)  # the ip instruction
data = [(x[0], int(x[1]), int(x[2]), int(x[3])) for x in data]
r = {
    0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f'
}
actions = {
    'add': '+',
    'mul': '*',
    'ban': '&',
    'bor': '|',
    'set': None,
    'gt': '>',
    'eq': '==',
}
for row, (i, a, b, c) in enumerate(data):
    print('%02d:  %4s %2s %2s %2s' % (row, i, a, b, c), end=' |   ')
    c = r[c]
    if i[-1] == 'r':
        b = r[b]
    for action, op in actions.items():
        if i.startswith(action):
            if action == 'set':
                if i[-1] == 'r':
                    a = r[a]
            elif len(action) == 3:
                a = r[a]
            elif len(action) == 2 and i[-2] == 'r':
                a = r[a]
            if action == 'set':
                print('%s = %s' % (c, a))
            else:
                print('%s = %s %s %s' % (c, a, op, b))
            break
