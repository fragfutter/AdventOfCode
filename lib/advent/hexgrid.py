# see https://www.redblobgames.com/grids/hexagons/


class HexCoordinates(object):
    def neighbours(self):
        yield(self.north())
        yield(self.northeast())
        yield(self.southeast())
        yield(self.south())
        yield(self.southwest())
        yield(self.northwest())


class Cube(HexCoordinates):
    """
      \ n  /
    nw +--+ ne
      /    \
    -+      +-
      \    /
    sw +--+ se
      / s  \

       +---+
      /x   z\
     +       +
      \  y  /
       +---+

    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def to_hex(self):
        return Hex(self.x, self.z)

    def to_cube(self):
        return self

    def north(self):
        return Cube(self.x, self.y + 1, self.z - 1)

    def south(self):
        return Cube(self.x, self.y - 1, self.z + 1)

    def northwest(self):
        return Cube(self.x - 1, self.y + 1, self.z)

    def southeast(self):
        return Cube(self.x + 1, self.y - 1, self.z)

    def northeast(self):
        return Cube(self.x + 1, self.y, self.z - 1)

    def southwest(self):
        return Cube(self.x - 1, self.y,  self.z + 1)

    def __eq__(self, other):
        if isinstance(other, Hex):
            other = other.to_cube()
        if isinstance(other, Cube):
            return \
                self.x == other.x and \
                self.y == other.y and \
                self.z == other.z
        return False


class Hex(HexCoordinates):
    """
       +---+
      /q   r\
     +       +
      \     /
       +---+
    """
    def __init__(self, q, r):
        self.q = q
        self.r = r

    def to_hex(self):
        return self

    def to_cube(self):
        x = self.q
        z = self.r
        # x + y + z = 0
        y = - z - x
        return Cube(x, y, z)

    def north(self):
        return Hex(self.q, self.r + 1)

    def south(self):
        return Hex(self.q, self.r - 1)

    def northeast(self):
        return Hex(self.q + 1, self.r + 1)

    def southwest(self):
        return Hex(self.q - 1, self.r - 1)

    def northwest(self):
        return Hex(self.q - 1, self.r)

    def southeast(self):
        return Hex(self.q + 1, self.r)

    def __eq__(self, other):
        if isinstance(other, Cube):
            other = other.to_hex()
        if isinstance(other, Hex):
            return \
                self.q == other.q and \
                self.r == other.r
        return False


def distance(a, b):
    a = a.to_cube()
    b = b.to_cube()
    result = \
        abs(abs(a.x) - abs(b.x)) + \
        abs(abs(a.y) - abs(b.y)) + \
        abs(abs(a.z) - abs(b.z))
    return abs(int(result/2))
