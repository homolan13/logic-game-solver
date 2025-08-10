from abc import ABC, abstractmethod
from copy import deepcopy

from logic_game_solver._template.state import GameState, FieldState
from logic_game_solver._template.exceptions import NoSolution, AmbiguousSolutions

class BaseGameEngine(ABC):
    """
    Base class for game engines in a logic game solver.
    """
    def __init__(self, game_state: GameState):
        """
        Initialize the game engine with a game state.
        
        :param game: An instance of GameState containing the initial game data.
        """
        for name, field in game_state.data.items():
            if isinstance(field.value, list):
                game_state.data[name].source = 'initial'  # Set the source of initial field states to 'initial'

        if not self.verify_game_state():
            raise ValueError('Game state is not consistent.')
        
        self.initial_game_state = deepcopy(game_state)  # Store the initial game state
        self.game_state = game_state
        self.step_count = 0  # Counter for the number of steps taken

        if self.is_solved():
            raise ValueError('Game is already solved.')
           
        self.step()  # Initialize the first step to enforce the rules on the initial field state spaces

    def step(self):
        """
        Perform a single step in the game engine (assign one field value and update field state spaces).
        """
        # Assign
        if self.is_solved() or not any(isinstance(field.value, list) for field in self.game_state.data.values()):
            raise ValueError('Game is already solved or no field state spaces to assign.')
        
        if not any(len([value for value in field.value if isinstance(value, list)]) == 1 for field in self.game_state.data.values()):
            raise AmbiguousSolutions('Multiple solutions found where only one is expected.')
        
        name = next(name for name, field in self.game_state.data.items() if isinstance(field.value, list) and len(field.value) == 1)
        value = self.game_state.data[name].value[0]  # Get the single value from the field state space
        self.game_state.data[name] = FieldState(value, self.solver)

        # Enforce
        for name, field in self.game_state.data.items():
            if isinstance(field.value, list):
                self.game_state.data[name] = self.enforce(name, field)  # Enforce the rules of the game on each field state

        self.step_count += 1

        if self.verify_game_state():
            raise ValueError('Game state is not consistent after enforcing rules.')

    def solve(self):
        """
        Solve the game using the game engine.
        """
        while not self.is_solved():
            self.step()
            if self.step_count > 1000:  # Arbitrary limit to prevent infinite loops
                raise NoSolution('No solution found within the step limit.')

    def reset(self, reset_count: bool = False):
        """
        Reset the game engine to its initial state.

        :param reset_count: If True, reset the step count to 0.
        """
        self.game_state = deepcopy(self.initial_game_state)
        if reset_count:
            self.step_count = 0

    def is_solved(self) -> bool:
        """
        Check if the game is solved.

        :return: True if the game is solved, False otherwise.
        """
        return not any(isinstance(field.value, list) for field in self.game_state.data.values())
    
    @property
    @abstractmethod
    def solver(self) -> str:
        """
        Return the name of the solver for this game engine.
        
        :return: The name of the solver.
        """
        raise NotImplementedError('This property should be implemented by subclasses.')

    @abstractmethod
    def enforce(self, name: str, field: FieldState) -> FieldState:
        """
        Enforce the rules of the game on one field.
        This method should be implemented by subclasses.

        :param name: The name of the field to enforce rules on.
        :param field: An instance of FieldState representing the field to enforce rules on.
        :return: The updated field state after enforcing the rules.
        """
        raise NotImplementedError('This method should be implemented by subclasses.')

    @abstractmethod
    def verify_game_state(self) -> bool:
        """
        Verify the current game state for consistency.

        :return: True if the game state is consistent, False otherwise.
        """
        raise NotImplementedError('This method should be implemented by subclasses.')
