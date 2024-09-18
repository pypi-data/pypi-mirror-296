from varphitape.model import TapeCharacter
from varphi.model import HeadDirection, Instruction, State


def test_instruction_initializer():
    """
    Test that the Instruction initializer works correctly.

    Use TapeCharacter.TALLY, pick a direction, and initialize the Instruction
    object. Check that its members are initialized as expected.
    """
    state = State()
    character = TapeCharacter.TALLY
    direction = HeadDirection.RIGHT
    instruction = Instruction(nextState=state,
                              characterToPlace=character,
                              directionToMove=direction)

    # Check that the members of the instruction are as expected
    assert instruction.nextState == state
    assert instruction.characterToPlace == character
    assert instruction.directionToMove == direction


def test_add_on_tally_instruction():
    """
    Test addOnTallyInstruction by adding instructions to the state.

    - Append an instruction and check that the length of onTally is 1.
    - Call the method again and check that the length is 2.
    """
    state = State()
    instruction1 = Instruction(nextState=State(),
                               characterToPlace=TapeCharacter.TALLY,
                               directionToMove=HeadDirection.RIGHT)
    instruction2 = Instruction(nextState=State(),
                               characterToPlace=TapeCharacter.BLANK,
                               directionToMove=HeadDirection.LEFT)

    # Add first instruction
    state.addOnTallyInstruction(instruction1)
    assert len(state.onTally) == 1

    # Add second instruction
    state.addOnTallyInstruction(instruction2)
    assert len(state.onTally) == 2


def test_add_on_blank_instruction():
    """
    Test addOnBlankInstruction by adding instructions to the state.

    - Append an instruction and check that the length of onBlank is 1.
    - Call the method again and check that the length is 2.
    """
    state = State()
    instruction1 = Instruction(nextState=State(),
                               characterToPlace=TapeCharacter.TALLY,
                               directionToMove=HeadDirection.RIGHT)
    instruction2 = Instruction(nextState=State(),
                               characterToPlace=TapeCharacter.BLANK,
                               directionToMove=HeadDirection.LEFT)

    # Add first instruction
    state.addOnBlankInstruction(instruction1)
    assert len(state.onBlank) == 1

    # Add second instruction
    state.addOnBlankInstruction(instruction2)
    assert len(state.onBlank) == 2
