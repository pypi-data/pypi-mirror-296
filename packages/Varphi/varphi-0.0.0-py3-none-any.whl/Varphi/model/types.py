from dataclasses import dataclass
from enum import Enum, auto

from VarphiTape.model import TapeCharacter

class HeadDirection(Enum):
    """
    Defines two directions that the head moves in.
    """
    LEFT = auto()
    RIGHT = auto()

@dataclass
class Instruction:
    """
    An instruction for a (possibly non-deterministic) Turing machine.
    """
    nextState: "State"  # The quotes around mean that this is a forward reference, since State is not yet defined here
    characterToPlace: TapeCharacter
    directionToMove: HeadDirection

@dataclass
class State:
    """
    A (potentially non-deterministic) Turing machine state.

    This class stores instructions for when tallies or blanks are encountered by the Turing machine head when the machine is on this state.
    """

    # The instruction (or instructions, for non-deterministic machines) that are followed if a tally or blank is seen while on this state. These are kept as a list, since Varphi supports non-deterministic machines
    onTally: list[Instruction]
    onBlank: list[Instruction]

    def __init__(self) -> None:
        self.onTally = []
        self.onBlank = []

    def addOnTallyInstruction(self, instruction: Instruction) -> None: 
        """
        Add an instruction to follow if a tally is seen by the head when the machine is on this state.

        Since non-deterministic machines are supported, calling this function twice will not remove the first instruction added.

            Parameters:
                instruction (Instruction): An instruction (potential, in the case of an NTM) to follow when a tally is encountered by the head while in this state.
        """
        self.onTally.append(instruction)
    
    def addOnBlankInstruction(self, instruction: Instruction) -> None:
        """
        Add an instruction to follow if a tally is seen by the head when the machine is on this state.

        Since non-deterministic machines are supported, calling this function twice will not remove the first instruction added.

            Parameters:
                instruction (Instruction): An instruction (potential, in the case of an NTM) to follow when a blank is encountered by the head while in this state.
        """        
        self.onBlank.append(instruction)
