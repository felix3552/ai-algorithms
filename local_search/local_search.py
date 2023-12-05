import random

from constraint import constraint


def domain(variable):
    return [1, 2, 3, 4]


# Generic local search algorithm
def local_search(variables, constraints):
    # Create random total assignment
    assignment = {}
    for variable in variables:
        assignment[variable] = random.choice(domain(variable))

    while not all([c.is_satisfied() for c in constraints]):
        # Pick a random variable and assign a random value to it
        variable = random.choice(variables)
        assignment[variable] = random.choice(domain(variable))

    return assignment


# Greedy Descent
def local_search_iterative(variables, constraints):
    # Create random total assignment
    assignment = {}
    for variable in variables:
        assignment[variable] = random.choice(domain(variable))

    return assignment


variables = ['A', 'B', 'C', 'D', 'E']
"""
B != 3
C != 2
A != B
B != C
C < D
A = D
E < A
E < B
E < C
E < D
B != D
"""
constraints = [
    constraint.Constraint(lambda x: x != 3, ['B']),
    constraint.Constraint(lambda x: x != 2, ['C']),
    constraint.Constraint(lambda x, y: x != y, ['A', 'B']),
    constraint.Constraint(lambda x, y: x != y, ['B', 'C']),
    constraint.Constraint(lambda x, y: x < y, ['C', 'D']),
    constraint.Constraint(lambda x, y: x == y, ['A', 'D']),
    constraint.Constraint(lambda x, y: x < y, ['E', 'A']),
    constraint.Constraint(lambda x, y: x < y, ['E', 'B']),
    constraint.Constraint(lambda x, y: x < y, ['E', 'C']),
    constraint.Constraint(lambda x, y: x < y, ['E', 'D']),
    constraint.Constraint(lambda x, y: x != y, ['B', 'D'])
]

print(local_search(variables, constraints))
