from lib import run_algorithm, Direction, GameState


def step(state: GameState):
    """
    This method is called every time the pawn is about to move.
    :param state: contains the state of the game. See readme.md for the available functions.
    :return: the direction in which the pawn has to move.
    """
    return simplestep(state)

def simplestep(state: GameState):
    """
    Simple algorithm
    """
    # If the cell below is free, go south
    if state.cell_safe(state.pawn_row() + 1, state.pawn_column()).is_empty():
        return Direction.SOUTH

    # If the cell to the right is free, go east
    if state.cell_safe(state.pawn_row(), state.pawn_column() + 1).is_empty():
        return Direction.EAST

    # If the cell above is free, go north
    if state.cell_safe(state.pawn_row() - 1, state.pawn_column()).is_empty():
        return Direction.NORTH

    # If the cell ot the left is free, go west
    if state.cell_safe(state.pawn_row(), state.pawn_column() - 1).is_empty():
        return Direction.WEST

    # Any normal print output is shown in the gameconsole.
    print("Oh no! Nowhere to go")

    # If nothing is returned, the pawn will move in the same direction as the previous step

def checkingstep(state: GameState):
    """
    Checks for non-wall entities
    """


run_algorithm(step)
