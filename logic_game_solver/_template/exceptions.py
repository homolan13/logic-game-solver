class NoSolution(Exception):
    """Raised when no solution is found for a given logic game."""
    pass

class AmbiguousSolutions(Exception):
    """Raised when multiple solutions are found where only one is expected."""
    pass
