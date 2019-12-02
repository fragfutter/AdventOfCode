from math import sqrt


class Node(object):
    """a node of a graph"""

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    @property
    def neighbours(self):
        """yield all neighbour nodes"""
        pass

    def distance(self, other):
        """distance to other node"""
        pass

    def distance_manhatten(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)

    def distance_diagonal(self, other):
        return max(abs(self.x - other.x), abs(self.y - other.y))

    def distance_euclid(self, other):
        return sqrt(
            (self.x - other.x)**2 +
            (self.y - other.y)**2
        )


class PriorityQueue(object):
    def __init__(self):
        self.data = []

    def push(self, node, meta):
        """add node and it's associated metadata"""
        self.data.append((node, meta))

    def pop(self):
        """remove and return node with lowest weight"""
        result = min(self.data, key=lambda node, meta: meta.estimate)
        self.data.remove(result)
        return result

    def __contains__(self, node):
        """test it item is in queue"""
        return node in self.data


class Astar(object):
    """
    Solve a graph using a* algorithm

    see https://en.wikipedia.org/wiki/A*_search_algorithm
    and http://www-m9.ma.tum.de/graph-algorithms/spp-a-star/index_de.html
    """
    def __init__(self, start, end):
        self.end = end
        self.seen = []  # list of visited nodes
        self.openlist = PriorityQueue()
        start.parent = None
        start.cost = 0
        start.estimate = self.heuristic(start)
        self.openlist.push(start)

    def heuristic(self, node):
        """estimates the cost reaching end from the given step,
        you might want to override this.

        May never underestimate the actual cost"""
        return self.end.distance(node)

    def is_solution(self, node):
        return self.end == node

    def solve(self):
        while self.openlist:
            current, current_meta = self.openlist.pop()
            self.seen.append(current)  # do not visit again
            if self.is_solution(current):
                return current
            for n in current.neighbours:
                if n in self.seen:
                    continue  # do not visit again
                if n in self.openlist:
                    # update if we find a shorter path
                    cost = current.cost + current.neighbours[n]
                    if n.cost > cost:
                        self.update_node(n, current)
                else:
                    self.update_node(n, current)
                    self.openlist.push(n)

    def update_node(self, node, parent):
        node.parent = parent
        node.cost = parent.cost + parent.neighbours[node]
        node.estimate = node.cost + self.heuristic(node)
