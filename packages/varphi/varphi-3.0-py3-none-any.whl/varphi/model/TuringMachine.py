import random

from .Head import Head
from .types import State
from varphitape.model import Tape, TapeCharacter

class TuringMachine:
    head: Head
    state: State

    def __init__(self, initialState: State) -> None:
        self.head = Head()
        self.state = initialState
    
    def execute(self, tape: Tape) -> None:
        """
        Run this Turing machine on the tape.
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

            # A non-deterministic choice is made to determine the execution path
            # If the Turing program corresponds to a deterministic machine, this choice will be deterministic, since onTally and onBlank contain only one instruction
            instruction = random.choice(self.state.onTally if tally else self.state.onBlank)
            self.state = instruction.nextState
            self.head.execute(instruction.characterToPlace, instruction.directionToMove, tape)
