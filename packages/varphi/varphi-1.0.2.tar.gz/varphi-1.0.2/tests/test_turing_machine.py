from varphi.model import TuringMachine, State, Instruction, HeadDirection
from varphitape.model import Tape, TapeCharacter


def test_add_one():
    q0 = State()
    qh = State()

    onTally = Instruction(q0, TapeCharacter.TALLY, HeadDirection.RIGHT)
    q0.addOnTallyInstruction(onTally)

    onBlank = Instruction(qh, TapeCharacter.TALLY, HeadDirection.LEFT)
    q0.addOnBlankInstruction(onBlank)

    # Initialize a tape to have four tallies
    tape = Tape()
    tape[0] = TapeCharacter.TALLY
    tape[1] = TapeCharacter.TALLY
    tape[2] = TapeCharacter.TALLY
    tape[3] = TapeCharacter.TALLY

    # Execute the turing machine on the tape and check that the result is 5
    turingMachine = TuringMachine(q0)
    turingMachine.execute(tape)
    assert tape[-1] == TapeCharacter.BLANK
    assert tape[0] == TapeCharacter.TALLY
    assert tape[1] == TapeCharacter.TALLY
    assert tape[2] == TapeCharacter.TALLY
    assert tape[3] == TapeCharacter.TALLY
    assert tape[4] == TapeCharacter.TALLY
    assert tape[5] == TapeCharacter.BLANK
