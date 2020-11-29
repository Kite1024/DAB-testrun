# Delft Algorithm Battle: Python Template

## Quickstart
1. Creating a repository [using this repo as a template](https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/creating-a-repository-from-a-template#creating-a-repository-from-a-template).
2. Connect your repo on te website.
3. Write your algorithm inside the `step()` function in `algorithm.py`.
4. Make sure your code is on the main branch of the repo.

Add any dependencies to the `requirements.txt` file.

## Reference 
    
### class GameState
This class represents gamefield at a certain moment.
It contains all the information you may need to choose what direction to point your pawn in.
Use the functions .field_width() and .field_height() to understand the size of the field.
The functions .pawn_row() and .pawn_column() will tell you where YOUR pawn is at.
With the function .cell(row, column) you can inspect any place on the board.

Methods defined here:

**cell(row: int, column: int) -> Cell**

    Given a row and column number, returns the Cell at that position.
    :param row must be between 0 and the field_height-1.
    :param column must be between 0 and the field_width-1.
    If the row and column are out of bounds it throws an exception.
    Use .cell_save() to get an wall cell when an out of bounds cell is requested.

**cell_safe(row: int, column: int) -> Cell**

    Given a row and column number, returns the cell at that position.
    In contrast to .cell(), this function does not throw an error if the row or column are out of bounds.
    Instead, it will return a cell occupied with a wall.

**field_height() -> int**

    Returns the number of vertical number of cells in this field. This is the number of rows the field has.

**field_width() -> int**

    Returns the number of cells that the field is wide. This is the number of columns this field has.

**is_alive() -> bool**

    Return whether or not the player pawn is in the field.
    If this is not the case the pawn has died.

**pawn_column() -> int**

    Returns the column at which the pawn controlled by this algorithm currently is or None when the pawn has died

**pawn_row() -> int**

    Returns the row at which the pawn controlled by this algorithm currently is or None when the pawn has died

### class Cell
A cell is a single position on the gamefield. Use the functions .is_occupied() and .is_empty() to determinate
if the cell is safe to move into. Be careful, if two pawns move into the same cell at the same time they both die.

If the cell is occupied, use .is_pawn() or .is_trail() to see what occupies it.

Use .char() to get a the raw character representation of the cell.

Methods defined here:

**char() -> str**
    Returns the raw character representation of the cell. The following values can be expected:
    
    .     Empty space. Will not kill you if you move into it.
    #     Wall. Will kill you if you move into them.
    a-Z   Each character is assigned a letter. The uppercase variant will make up the head and the lowercase
          variant the tail. I.e. if a team is assigned 'N', their head in the field is 'N' and their tail 'n'.
    *     Special death-case: a cell has the star when some special death happened.
          For example if two players tried to move into the same space or if a player's algorithm lost connection.

**is_empty() -> bool**

    Returns True if the cell is not occupied.
    It is safe to move into this cell, unless another pawn does so as well.

**is_occupied() -> bool**

    Returns True if the cell is not empty. Moving into an occupied cell will kill the pawn.

**is_pawn() -> bool**

    Returns True if the cell is occupied with any pawn.
    Also returns True if the cell is occupied with your pawn.

**is_trail() -> bool**

    Returns True if the cell is occupied with the trail of a pawn.

**is_wall() -> bool**

    Returns True if this cell occupied with a wall. Don't move into this.
