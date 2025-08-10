from logic_game_solver._template import BaseGameEngine, FieldState


class SudokuEngine(BaseGameEngine):
    """
    Engine for solving the Sudoku game.
    Inherits from BaseGameEngine and implements specific rules for Sudoku.
    """
    @property
    def solver(self):
        """
        Returns the solver instance associated with this engine.
        """
        return self.__class__.__name__  # 'SudokuEngine'

    def enforce(self, name: str, field: FieldState) -> FieldState:
        """
        Enforce the rules of the Sudoku game on the given field state.
        
        :param name: The name of the field to enforce rules on.
        :param field: The current state of the field.
        :return: Updated FieldState after enforcing the rules.
        """
        pass

    def verify_game_state(self) -> bool:
        """
        Verify the current game state for consistency.
        
        :return: True if the game state is consistent, False otherwise.
        """
        pass
    