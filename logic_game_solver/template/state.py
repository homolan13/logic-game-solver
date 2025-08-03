class GameState():
    """
    Class for game states in a logic game solver.
    """
    def __init__(self, data: dict, state: str):
        self.data = data  # dict with game data (keys: fields, values: field states)
        self.state = state  # 'solved' or 'unsolved'


class FieldState():
    """
    Class for field states in a logic game solver.
    """
    def __init__(self, value: list | int | float, source: str):
        self.value = value
        self.source = source
        