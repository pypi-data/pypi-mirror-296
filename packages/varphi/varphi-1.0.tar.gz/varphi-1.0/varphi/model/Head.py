from .types import HeadDirection, TapeCharacter
from varphi_tape.model import Tape, TapeCharacter

class Head:
    tapeIndex: int  # The index of the tape cell that this head is currently stationed at

    def __init__(self):
        self.tapeIndex = 0

    def execute(self, characterToPlace: TapeCharacter, directionToMove: HeadDirection, tape: Tape) -> None:
        """
        Place a character at the cell that this head is currently stationed at and move in a certain direction.
        """
        tape[self.tapeIndex] = characterToPlace
        self.tapeIndex += 1 if directionToMove == HeadDirection.RIGHT else -1

    def read(self, tape: Tape) -> TapeCharacter:
        """
        Return the character at the cell that this head is currently stationed at. 
        """
        return tape[self.tapeIndex]
