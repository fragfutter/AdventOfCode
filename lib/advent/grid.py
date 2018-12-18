class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return '<Point %d, %d>' % (self.x, self.y)

    def distance(self, other):
        """manhatten distance"""
        return \
            abs(self.x - other.x) + \
            abs(self.y - other.y)

    def north(self):
        return Point(self.x, self.y + 1)

    def south(self):
        return Point(self.x, self.y - 1)

    def east(self):
        return Point(self.x + 1, self.y)

    def west(self):
        return Point(self.x - 1, self.y)

    def northwest(self):
        return Point(self.x - 1, self.y + 1)

    def northeast(self):
        return Point(self.x + 1, self.y + 1)

    def southwest(self):
        return Point(self.x - 1, self.y - 1)

    def southeast(self):
        return Point(self.x + 1, self.y - 1)

    def neighbours(self, diagonal=True):
        yield self.north()
        yield self.south()
        yield self.east()
        yield self.west()
        if diagonal:
            yield self.northwest()
            yield self.northeast()
            yield self.southwest()
            yield self.southeast()
