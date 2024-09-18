import random

from .Head import Head
from .types import State
from varphitape.model import Tape, TapeCharacter


class TuringMachine:
    """
    A class representing a Turing machine, which processes a tape based on its
    current state and head position.

    Attributes:
        - head (Head): The head of the Turing machine, responsible for reading
          and writing on the tape.
        - state (State): The current state of the Turing machine, determining
          its behavior based on the tape's symbols.
    """

    head: Head
    state: State

    def __init__(self, initialState: State) -> None:
        """
        Initialize the Turing machine with an initial state.

        Args:
            - initialState (State): The starting state of the Turing machine.
        """
        self.head = Head()
        self.state = initialState

    def execute(self, tape: Tape) -> None:
        """
        Run the Turing machine on the given tape. The machine reads symbols
        from the tape, updates the tape based on the current stat, and moves
        the head accordingly. It stops when there are no more transitions
        defined for the current state and symbol.

        Args:
            - tape (Tape): The tape on which the Turing machine operates.

        Returns:
            None
        """
        while True:
            tally = False
            if self.head.read(tape) == TapeCharacter.TALLY:
                if len(self.state.onTally) == 0:
                    return
                tally = True
            else:
                if len(self.state.onBlank) == 0:
                    return

            # A non-deterministic choice is made to determine the execution
            # path
            # If the Turing program corresponds to a deterministic machine,
            # this choice will be deterministic, since onTally and onBlank
            # contain only one instruction
            instructions = self.state.onTally if tally else self.state.onBlank
            instruction = random.choice(instructions)
            self.state = instruction.nextState
            self.head.execute(instruction.characterToPlace,
                              instruction.directionToMove,
                              tape)
