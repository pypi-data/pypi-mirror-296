from varphi.model import Head, HeadDirection
from varphitape.model import Tape, TapeCharacter


def test_head():
    tape = Tape()
    head = Head()

    # Read index 0 on the tape
    assert head.read(tape) == TapeCharacter.BLANK

    # Put a tally at index 0
    tape[0] = TapeCharacter.TALLY

    # Read again, should be a tally
    assert head.read(tape) == TapeCharacter.TALLY

    # Now put blank and move to the right
    head.execute(TapeCharacter.BLANK, HeadDirection.RIGHT, tape)

    # Index 0 should now have blank
    assert tape[0] == TapeCharacter.BLANK

    # Now put a tally at index 1 and move to the left
    head.execute(TapeCharacter.TALLY, HeadDirection.LEFT, tape)

    # Index 1 should have tally
    assert tape[1] == TapeCharacter.TALLY

    # One more time, write tally and move left
    head.execute(TapeCharacter.TALLY, HeadDirection.LEFT, tape)

    # Index 0 should have tally
    assert tape[0] == TapeCharacter.TALLY
