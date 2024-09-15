from .VarphiTapeParser import VarphiTapeParser
from .VarphiTapeListener import VarphiTapeListener
from varphi_tape.model import Tape, TapeCharacter


TALLY_CHARACTERS = {'1', 'I', 'i', '|'}
BLANK_CHARACTERS = {' ', '\t', '\n', '\r', '_', '-', '0', 'O', 'o', 'b', 'B'}


class VarphiTapeEvaluator(VarphiTapeListener):
    """
    A listener that evaluates a parsed tape.

    The evaluator listens for tape symbols (TALLY or BLANK) and updates the Tape model accordingly.
    
    Attributes:
    - tape (Tape): The current state of the Turing machine tape.
    """
    tape: Tape

    def __init__(self) -> None:
        """
        Initializes the evaluator with an empty tape.
        """
        self.tape = Tape()
        super().__init__()
    
    def enterTape(self, ctx:VarphiTapeParser.TapeContext) -> None:
        """
        Populates the tape with characters (TALLY or BLANK) from the parsed input.
        
        Args:
        - ctx (VarphiTapeParser.TapeContext): The context for the tape rule in the parser.
        """
        # Loop through each TAPE_SYMBOL
        for i in range(ctx.getChildCount() - 1):
            symbol = ctx.getChild(i).getText()
            if symbol in TALLY_CHARACTERS:
                self.tape[i] = TapeCharacter.TALLY
            elif symbol in BLANK_CHARACTERS:
                self.tape[i] = TapeCharacter.BLANK
