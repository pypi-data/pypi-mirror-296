from model.types import *
from model.TuringMachine import TuringMachine
from model.types import TapeCharacter

def numberOfOnesOnTape(machine: TuringMachine) -> int:
    numOnes = 0
    for i in range(machine.tape._maxLeftIndex, machine.tape._maxRightIndex + 1):
        if machine.tape[i] == TapeCharacter.TALLY:
            numOnes += 1
    return numOnes
    

def test_plus_1():
    q0 = State()
    q1 = State()
    q0.addOnTallyInstruction(Instruction(q0, TapeCharacter.TALLY, HeadDirection.RIGHT))  # q0 1 q0 1 R
    q0.addOnBlankInstruction(Instruction(q1, TapeCharacter.TALLY, HeadDirection.LEFT))  # q0 b q1 1 L
    turingMachine = TuringMachine([5], q0)
    assert numberOfOnesOnTape(turingMachine) == 5
    turingMachine.execute()
    assert numberOfOnesOnTape(turingMachine) == 6


def test_non_deterministic():
    q0 = State()
    q1 = State()
    q2 = State()
    q0.addOnTallyInstruction(Instruction(q0, TapeCharacter.TALLY, HeadDirection.RIGHT))
    q0.addOnBlankInstruction(Instruction(q1, TapeCharacter.TALLY, HeadDirection.RIGHT))
    q1.addOnBlankInstruction(Instruction(q2, TapeCharacter.TALLY, HeadDirection.RIGHT))
    q1.addOnBlankInstruction(Instruction(q0, TapeCharacter.TALLY, HeadDirection.RIGHT))
    for _ in range(10000):
        turingMachine = TuringMachine([2], q0)
        assert numberOfOnesOnTape(turingMachine) == 2
        turingMachine.execute()
        numOnes = numberOfOnesOnTape(turingMachine)
        i = 1
        while True:
            if 2 + i * 2 == numOnes:
                break
            i += 1
