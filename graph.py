from collections import deque
from queue import PriorityQueue


class Stack:
    def __init__(self):
        self.stack = deque()

    def add(self, item):
        self.stack.appendleft(item)

    def remove(self):
        return self.stack.popleft()

    def is_not_empty(self):
        return len(self.stack) > 0


class StackWithMaxDepth:
    def __init__(self, max_depth):
        self.max_depth = max_depth
        self.stack = deque()

    def add(self, path):
        if len(path) - 1 > self.max_depth:
            return

        self.stack.appendleft(path)

    def remove(self):
        return self.stack.popleft()

    def is_not_empty(self):
        return len(self.stack) > 0


class Queue:
    def __init__(self):
        self.queue = deque()

    def add(self, item):
        self.queue.append(item)

    def remove(self):
        return self.queue.popleft()

    def is_not_empty(self):
        return len(self.queue) > 0


# Priority queue that sorts by weight of path
class PriorityQueuePathWeight:
    def __init__(self):
        self.queue = PriorityQueue()

    # We need to add a weight to the node
    # We calculate weight as the sum of the weights of the path
    def add(self, path):
        self.queue.put((path_cost(path), path), True)

    def remove(self):
        _, item = self.queue.get(True)
        return item

    def is_not_empty(self):
        # Waits until all queued items are processed

        return self.queue.qsize() > 0


# Priority queue that sorts by heuristic value of node
class PriorityQueueHeuristic:
    def __init__(self):
        self.queue = PriorityQueue()

    # We need to add a weight to the node
    # We calculate weight as the heuristic of the last node of the path
    def add(self, path):
        self.queue.put((h(path[-1]), path), True)

    def remove(self):
        _, item = self.queue.get(True)
        return item

    def is_not_empty(self):
        # Waits until all queued items are processed

        return self.queue.qsize() > 0


# Priority queue that sorts by f value of node
class PriorityQueueFValue:
    def __init__(self):
        self.queue = PriorityQueue()

    # We need to add a weight to the node
    # We calculate weight as the heuristic of the last node of the path
    def add(self, path):
        heuristic = h(path[-1])
        self.queue.put((heuristic + path_cost(path), path), True)

    def remove(self):
        _, item = self.queue.get(True)
        return item

    def is_not_empty(self):
        # Waits until all queued items are processed

        return self.queue.qsize() > 0


# Returns the heuristic value of a node
def h(node):
    heuristics = {
        'S': 0,
        'A': 21,
        'B': 19,
        'C': 19,
        'D': 9,
        'F': 12,
        'E': 11,
        'G': 4,
        'H': 6,
        'Z': 0
    }
    return heuristics[node]


# Returns the weight value of the edge
def path_cost(path):
    edges = {
        ('S', 'A'): 3,
        ('S', 'B'): 9,
        ('S', 'C'): 4,
        ('A', 'C'): 2,
        ('B', 'C'): 13,
        ('C', 'D'): 5,
        ('C', 'E'): 4,
        ('C', 'F'): 8,
        ('D', 'F'): 5,
        ('E', 'F'): 7,
        ('F', 'G'): 8,
        ('F', 'H'): 7,
        ('F', 'Z'): 18,
        ('G', 'Z'): 9,
        ('H', 'Z'): 6
    }
    w = 0
    for i in range(len(path) - 1, 0, -1):
        w += edges[path[i - 1], path[i]]

    return w


# Directed graph with weighted edges represented as adjacency list
g = {
    'S': ['A', 'B', 'C'],
    'A': ['C'],
    'B': ['C'],

    'C': ['D', 'E', 'F'],
    'D': ['F'],
    'E': ['F'],

    'F': ['G', 'H', 'Z'],
    'G': ['Z'],
    'H': ['Z']
}

'''
Inputs:
• a graph
• a start node s
• Boolean procedure goal(n) to test if n is a goal
frontier <-- [<s>]
    while frontier is not empty
    select and remove path <no,....,nk> from frontier
    if goal(nk)
        return <no,....,nk>
    for every neighbor n of nk
        add <no,....,nk, n> to frontier
return NULL
'''


# Generic search algorithm
def search(graph, start, goal, frontier):
    frontier.add([start])

    while frontier.is_not_empty():
        path = frontier.remove()

        node = path[-1]
        print("Expand:", node)
        if node == goal:
            print("Goal found:", path)
            return path
        for neighbor in graph[node]:
            frontier.add(path + [neighbor])

    print("No path found from", start, "to", goal)
    return None


# Branch and bound, modified from generic search
# Only difference is that we don't return when we find the goal, and we prune all worse paths after the goal
def BandB(graph, start, goal, frontier):
    frontier.add([start])
    solution = None
    upper_bound = float('inf')

    while frontier.is_not_empty():
        path = frontier.remove()

        # We don't visit the path if it's worse or the same cost the solution
        if path_cost(path) > upper_bound:
            continue

        node = path[-1]
        print("Expand:", node)
        if node == goal:
            print("Goal found:", path)
            if path_cost(path) < upper_bound:
                solution = path
                upper_bound = path_cost(path)

            continue

        for neighbor in graph[node]:
            frontier.add(path + [neighbor])

    return solution


def ids(graph, start, goal):
    depth = 1
    while True:
        print("Depth:", depth)
        path = search(graph, start, goal, StackWithMaxDepth(depth))

        if path:
            return path
        depth += 1


# BFS
search(g, 'S', 'Z', Queue())

# DFS
search(g, 'S', 'Z', Stack())

# IDS
ids(g, 'S', 'Z')

# LCFS
search(g, 'S', 'Z', PriorityQueuePathWeight())

# BestFS
search(g, 'S', 'Z', PriorityQueueHeuristic())

# A*
search(g, 'S', 'Z', PriorityQueueFValue())

# B&B
BandB(g, 'S', 'Z', Stack())
