from .types import HeadDirection
from varphitape.model import Tape, TapeCharacter


class Head:
    """
    Represents the head of a Turing machine, responsible for reading and
    writing characters on the tape and moving in specified directions.

    Attributes:
        - tapeIndex (int): The current index on the tape where the head is
          located.
    """

    tapeIndex: int

    def __init__(self):
        """
        Initialize the Head at the starting position (index 0) on the tape.
        """
        self.tapeIndex = 0

    def execute(self,
                characterToPlace: TapeCharacter,
                directionToMove: HeadDirection,
                tape: Tape) -> None:
        """
        Place a character at the current position of the head on the tape and
        move the head in the specified direction.

        Args:
            - characterToPlace (TapeCharacter): The character to be placed on
              the tape at the current position.
            - directionToMove (HeadDirection): The direction in which to move
              the head (either LEFT or RIGHT).
            - tape (Tape): The tape on which the character is placed and the
              head moves.

        Returns:
            None
        """
        tape[self.tapeIndex] = characterToPlace
        self.tapeIndex += 1 if directionToMove == HeadDirection.RIGHT else -1

    def read(self, tape: Tape) -> TapeCharacter:
        """
        Read and return the character at the current position of the head on
        the tape.

        Args:
            - tape (Tape): The tape from which the character is read.

        Returns:
            TapeCharacter: The character at the current head position on the
            tape.
        """
        return tape[self.tapeIndex]
