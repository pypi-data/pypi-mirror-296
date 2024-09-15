from model.Tape import Tape
from model.types import TapeCharacter

def test_tape_no_initial_value():
    tape = Tape([])
    assert tape._maxRightIndex == 0
    assert tape._maxLeftIndex == 0
    assert tape.__str__() == "[...b...]"

def test_tape_single_initial_value_single_tick():
    tape = Tape([1])
    assert tape._maxRightIndex == 0
    assert tape._maxLeftIndex == 0
    assert tape.__str__() == "[...I...]"

def test_tape_single_initial_value():
    tape = Tape([3])
    assert tape._maxRightIndex == 2
    assert tape._maxLeftIndex == 0
    assert tape.__str__() == "[...I,I,I...]"

def test_tape_multiple_initial_values():
    tape = Tape([1,2,3])
    assert tape._maxRightIndex == 7
    assert tape._maxLeftIndex == 0
    assert tape.__str__() == "[...I,b,I,I,b,I,I,I...]"

def test_tape_initial_value_zero():
    tape = Tape([0])
    assert tape._maxRightIndex == 0
    assert tape._maxLeftIndex == 0
    assert tape.__str__() == "[...b...]"

def test_tape_initial_multiple_values_zero():
    tape = Tape([0,0,0])
    assert tape._maxRightIndex == 2
    assert tape._maxLeftIndex == 0
    assert tape.__str__() == "[...b,b,b...]"

def test_tape_initial_values_positive_and_0():
    tape = Tape([1,0,2,0,3])
    assert tape._maxRightIndex == 9
    assert tape._maxLeftIndex == 0
    assert tape.__str__() == "[...I,b,b,I,I,b,b,I,I,I...]"

def test_tape_getitem():
    tape = Tape([1,0,2,0,3])
    assert tape[0] == TapeCharacter.TALLY
    assert tape[1] == TapeCharacter.BLANK
    assert tape[-2] == TapeCharacter.BLANK
    assert tape._maxLeftIndex == -2