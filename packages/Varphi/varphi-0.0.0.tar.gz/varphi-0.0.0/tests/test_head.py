from model.Head import Head
from model.Tape import Tape
from model.types import HeadDirection, TapeCharacter


def test_execute():
    tape = Tape([])
    head = Head()
    head.execute(TapeCharacter.TALLY, HeadDirection.LEFT, tape)
    assert tape.__str__() == "[...I...]"
    head.execute(TapeCharacter.BLANK, HeadDirection.LEFT, tape)
    assert tape.__str__() == "[...b,I...]"

def test_read():
    tape = Tape([])
    head = Head()
    assert head.read(tape) == TapeCharacter.BLANK
    tape[0] = TapeCharacter.TALLY
    assert head.read(tape) == TapeCharacter.TALLY
    head.execute(TapeCharacter.TALLY, HeadDirection.LEFT, tape)
    assert head.read(tape) == TapeCharacter.BLANK
