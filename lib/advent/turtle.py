from itertools import cycle

N = (0, 1)
S = (0, -1)
W = (-1, 0)
E = (1, 0)


class Turtle(object):
    def __init__(self, position=(0, 0)):
        self.steps = 0
        self.directions = cycle((S, E, N, W))
        self.turn()
        self.position = position

    def turn(self):
        self.direction = next(self.directions)

    def walk(self):
        self.position = tuple(map(sum, zip(self.position, self.direction)))
        self.steps += 1

    def neighbours(self):
        """neighbours in all directions including diagonals"""
        x, y = self.position
        yield (x + 1, y)
        yield (x - 1, y)
        yield (x, y + 1)
        yield (x, y - 1)
        yield (x + 1, y + 1)
        yield (x - 1, y + 1)
        yield (x + 1, y - 1)
        yield (x - 1, y - 1)

    def left(self):
        """coordinates left of current position"""
        x, y = self.position
        m = {
            S: (x + 1, y),
            E: (x, y + 1),
            N: (x - 1, y),
            W: (x, y - 1),
        }
        return m[self.direction]


if __name__ == '__main__':
    t = Turtle()
    data = {}
    for i in range(23):
        print(t.position, ' => ', t.steps)
        data[t.position] = t.steps
        if t.left() not in data:
            print('turning')
            t.turn()
        t.walk()
