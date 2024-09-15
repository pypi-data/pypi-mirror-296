from varphi.model.Head import Head
from varphi.model.types import HeadDirection
from varphitape.model import Tape, TapeCharacter


def test_execute():
    tape = Tape()
    head = Head()
    head.execute(TapeCharacter.TALLY, HeadDirection.LEFT, tape)
    assert tape.__str__() == "1"
    head.execute(TapeCharacter.BLANK, HeadDirection.LEFT, tape)
    assert tape.__str__() == "01"

def test_read():
    tape = Tape()
    head = Head()
    assert head.read(tape) == TapeCharacter.BLANK
    tape[0] = TapeCharacter.TALLY
    assert head.read(tape) == TapeCharacter.TALLY
    head.execute(TapeCharacter.TALLY, HeadDirection.LEFT, tape)
    assert head.read(tape) == TapeCharacter.BLANK
