import sys
import traceback
from enum import Enum


# Stdout must only be used to communicate to the game-engine
# The following code ensures calls to print() wil end up in stderr.
_stdout = sys.stdout
_stderr = sys.stderr
sys.stdout = _stderr


def print_stdout(line: str):
    """
    Stdout must only be used to communicate to the game-engine.
    Stderr must be used for any other (debug) messages.
    Therefore the sys.stdout (used by print()) is set to output to stderr
    This method is used to send something on stdout.
    """
    print(line, file=_stdout, flush=True)


class Direction(Enum):
    NORTH = 'north'
    EAST = 'east'
    SOUTH = 'south'
    WEST = 'west'


class Cell:
    """
    A cell is a single position on the gamefield. Use the functions .is_occupied() and .is_empty() to determinate
    if the cell is safe to move into. Be careful, if two pawns move into the same cell at the same time they both die.

    If the cell is occupied, use .is_pawn() or .is_trail() to see what occupies it.

    Use .char() to get a the raw character representation of the cell.
    """

    def __init__(self, char: str, ):
        self._char = char

    def is_occupied(self) -> bool:
        """Returns True if the cell is not empty. Moving into an occupied cell will kill the pawn."""
        return self._char != '.'

    def is_empty(self) -> bool:
        """Returns True if the cell is not occupied.
        It is safe to move into this cell, unless another pawn does so as well."""
        return self._char == '.'

    def is_pawn(self) -> bool:
        """Returns True if the cell is occupied with any pawn.
        Also returns True if the cell is occupied with your pawn."""
        return self._char.isupper()

    def is_trail(self) -> bool:
        """Returns True if the cell is occupied with the trail of a pawn."""
        return self._char.islower() or self._char == "*"

    def is_wall(self) -> bool:
        """Returns True if this cell occupied with a wall. Don't move into this."""
        return self._char == '#'

    def char(self) -> str:
        """
        Returns the raw character representation of the cell. The following values can be expected:

        .     Empty space. Will not kill you if you move into it.
        #     Wall. Will kill you if you move into them.
        a-Z   Each character is assigned a letter. The uppercase variant will make up the head and the lowercase
              variant the tail. I.e. if a team is assigned 'N', their head in the field is 'N' and their tail 'n'.
        *     Special death-case: a cell has the star when some special death happened.
              For example if two players tried to move into the same space or if a player's algorithm lost connection.
        """
        return self._char


class GameState:
    """
    This class represents gamefield at a certain moment.
    It contains all the information you may need to choose what direction to point your pawn in.
    Use the functions .field_width() and .field_height() to understand the size of the field.
    The functions .pawn_row() and .pawn_column() will tell you where YOUR pawn is at.
    With the function .cell(row, column) you can inspect any place on the board.
    """

    def __init__(self, line: str, width: int, height: int, pawn_char: str):
        self._field_width = width
        self._field_height = height
        self._field = []
        self._pawn_row = None
        self._pawn_col = None

        self._alive = False
        for row in range(height):
            self._field.append([])
            for col in range(width):
                c = line[row * width + col]
                self._field[row].append(Cell(c))
                if c == pawn_char:
                    self._alive = True
                    self._pawn_row = row
                    self._pawn_col = col

    def cell(self, row: int, column: int) -> Cell:
        """
        Given a row and column number, returns the cell at that position.
        :param row must be between 0 and the field_height-1.
        :param column must be between 0 and the field_width-1.
        If the row and column are out of bounds it throws an exception.
        Use .cell_save() to get an wall cell when an out of bounds cell is requested.
        """
        if row >= self._field_height:
            raise ValueError("While calling the .cell() method, a row value of " +
                             str(row) + " was entered. This is is too large. "
                                        "It must be smaller than the height of the field (" + str(self._field_height) + ")")
        if column >= self._field_width:
            raise ValueError("While calling the .cell() method, a column value of " +
                             str(column) + " was entered. This is is too large. "
                             "It must be smaller than the width of the field (" + str(self._field_width) + ")")
        if row < 0:
            raise ValueError("While calling the .cell() method, a row value smaller than 0 was entered. " +
                             "It was " + str(row) + ".")
        if column < 0:
            raise ValueError("While calling the .cell() method, a column value smaller than 0 was entered. " +
                             "It was " + str(column) + ".")

        return self._field[row][column]

    def cell_safe(self, row: int, column: int) -> Cell:
        """
        Given a row and column number, returns the cell at that position.
        In contrast to .cell(), this function does not throw an error if the row or column are out of bounds.
        Instead, it will return a cell occupied with a wall.
        """
        if row >= self._field_height or column >= self._field_width or row < 0 or column < 0:
            return Cell('#')
        return self._field[row][column]

    def field_width(self) -> int:
        """Returns the number of cells that the field is wide. This is the number of columns this field has."""
        return self._field_width

    def field_height(self) -> int:
        """Returns the number of vertical number of cells in this field. This is the number of rows the field has."""
        return self._field_height

    def pawn_row(self) -> int:
        """Returns the row at which the pawn controlled by this algorithm currently is or None when the pawn has died"""
        return self._pawn_row

    def pawn_column(self) -> int:
        """Returns the column at which the pawn controlled by this algorithm currently is or None when the pawn has died"""
        return self._pawn_col

    def is_alive(self) -> bool:
        """
        Return whether or not the player pawn is in the field.
        If this is not the case the pawn has died.
        """
        return self._alive


def run_algorithm(step):
    """
    Waits for level-updates, calls the given step function accordingly and sends directional updates to the game-engine.
    :param step:
    :return:
    """
    first_line = sys.stdin.readline().strip()
    parts = first_line.split('|')
    pawn = parts[0]
    map_width = int(parts[1])
    map_height = int(parts[2])

    for line in sys.stdin:
        # Remove trailing newline
        line = line.strip()

        # Decode the line
        state = GameState(line, map_width, map_height, pawn)

        if not state.is_alive():
            print("My pawn was not found in the map. Assuming it died. Exiting algorithm.")
            return

        try:
            next_step = step(state)
            if not isinstance(next_step, Direction):
                raise ValueError("The method .step() returned a non-direction value."
                                 "It must return Direction.NORTH, Direction.EAST, Direction.SOUTH or Direction.WEST")

            print_stdout(pawn + ":" + str(next_step.value))
        except:
            print("An error occurred while executing a step of the algorithm. The error was:")
            print(traceback.format_exc())
