from collections import defaultdict
from enum import Enum


class TapeCharacter(Enum):
    """
    Enum class defining the allowed tape characters in the Varphi language.
    
    TapeCharacter represents a unary Turing machine's tape symbol:
    
    - `BLANK`: Represented as 0, indicates the absence of a tally mark.
    - `TALLY`: Represented as 1, indicates the presence of a tally mark.
    """
    BLANK = 0
    TALLY = 1


class Tape:
    """
    A class representing the tape of a Turing machine.
    
    The tape is modeled as an infinite list of cells, each of which can hold either a tally mark or a blank.
    The index 0 represents the initial cell, with positive and negative indices representing cells to the right and left, respectively.

    Attributes:
    - `_contents` (dict[int, TapeCharacter]): Stores tape characters at different positions, defaulting to BLANK for uninitialized cells.
    - `_maxRightIndex` (int): The furthest right cell that has been accessed or written to, default -inf
    - `_maxLeftIndex` (int): The furthest left cell that has been accessed or written to, default inf
    """
    _contents: dict[int, TapeCharacter]
    _maxRightIndex: int | float
    _maxLeftIndex: int | float

    def __init__(self):
        """
        Initializes the tape with all cells set to BLANK.
        """
        self._contents = defaultdict(lambda: TapeCharacter.BLANK)  # The tape will be filled with blanks initially
        self._maxRightIndex = float("-inf")
        self._maxLeftIndex = float("inf")

    def __getitem__(self, index: int) -> TapeCharacter:
        """
        Returns the tape character at a specific index.
        
        Args:
        - index (int): The index of the cell to retrieve.
        
        Returns:
        - TapeCharacter: The tape character at the specified index.
        """
        # Update the max indices if the desired index exceeds them
        if index > self._maxRightIndex: 
            self._maxRightIndex = index
        elif index < self._maxLeftIndex:
            self._maxLeftIndex = index
        return self._contents[index]
    
    def __setitem__(self, index: int, value: TapeCharacter):
        """
        Sets the tape character at a specific index.
        
        Args:
        - index (int): The index of the cell to set.
        - value (TapeCharacter): The character (TALLY or BLANK) to place in the cell.
        """
        # Update the max indices if the desired index exceeds them
        if index > self._maxRightIndex: 
            self._maxRightIndex = index
        elif index < self._maxLeftIndex:
            self._maxLeftIndex = index
        self._contents[index] = value

    def __repr__(self):
        """
        Provides a string representation of the current tape state.
        
        Returns:
        - str: A string showing the contents of the tape from the minimum accessed index to the maximum accessed index.
        """
        # Do not print anything if maxLeftIndex or maxRightIndex are infinite
        if self._maxLeftIndex > self._maxRightIndex:
            return ''
        return ''.join(str(self._contents[i].value) for i in range(self._maxLeftIndex, self._maxRightIndex + 1))
