class Constraint:
    def __init__(self, constraint, arguments):
        self.constraint = constraint
        self.arguments = arguments

    def holds(self, assignment):

        # If we haven't created a world yet with the variables then we can't check the constraint thus we return True
        for argument in self.arguments:
            if argument not in assignment:
                return True
        match len(self.arguments):
            case 1:

                return self.constraint(
                    assignment[self.arguments[0]]
                )
            case 2:
                return self.constraint(
                    assignment[self.arguments[0]],
                    assignment[self.arguments[1]]
                )
            case _:
                raise Exception('Invalid number of arguments')
