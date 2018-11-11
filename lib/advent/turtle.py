class Direction(object):
    directions = (
        (0, 1),  # N
        (1, 0),  # E
        (0, -1),  # S
        (-1, 0),  # W
    )
    instances = {}  # dict of direction => object

    def __new__(cls, x, y):
        d = (x, y)
        try:
            return cls.instances[d]
        except KeyError:
            result = super().__new__(cls)
            result.d = d
            cls.instances[d] = result
            return result

    def _turn(self, steps):
        d = self.directions[self.directions.index(self.d) - steps]
        try:
            return self.instances[d]
        except KeyError:
            return Direction(d)

    @property
    def left(self):
        return self._turn(1)

    @property
    def around(self):
        return self._turn(2)

    @property
    def right(self):
        return self._turn(3)

    def walk(self, position, steps=1):
        """create new position by walking N steps in our direction"""
        x = position[0] + steps * self.d[0]
        y = position[1] + steps * self.d[1]
        return (x, y)


N = Direction(0, 1)
E = Direction(1, 0)
S = Direction(0, -1)
W = Direction(-1, 0)


class Turtle(object):
    def __init__(self, position=(0, 0), direction=S):
        self.steps = 0
        self.direction = direction
        self.position = position

    def turn_left(self):
        """change direction by turning left"""
        self.direction = self.direction.left

    def turn_right(self):
        """change direction by turning right"""
        self.direction = self.direction.right

    def turn_around(self):
        """change direction by turning around"""
        self.direction = self.direction.around

    def walk(self):
        self.position = self.direction.walk(self.position)
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
        return self.direction.left.walk(self.position)


if __name__ == '__main__':
    assert(N.left == W)
    assert(N.right == E)
    assert(N.around == S)
    assert(W.left == S)
    assert(W.right == N)
    assert(W.around == E)
    assert(S.left == E)
    assert(S.right == W)
    assert(S.around == N)
    assert(E.left == N)
    assert(E.right == S)
    assert(E.around == W)

    t = Turtle(direction=N)
    t.walk()
    assert(t.position == (0, 1))
    t.turn_right()
    t.walk()
    assert(t.position == (1, 1))
    t.turn_right()
    t.walk()
    assert(t.position == (1, 0))
    t.turn_right()
    t.walk()
    assert(t.position == (0, 0))
    t.turn_left()
    t.walk()
    assert(t.position == (0, -1))
    t.turn_left()
    t.walk()
    assert(t.position == (1, -1))
    t.turn_left()
    t.walk()
    assert(t.position == (1, 0))
