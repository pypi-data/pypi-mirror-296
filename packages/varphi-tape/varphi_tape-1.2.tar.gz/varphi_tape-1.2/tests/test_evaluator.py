from antlr4 import *

from varphi_tape.antlr import VarphiTapeLexer, VarphiTapeParser, VarphiTapeEvaluator
from varphi_tape.model import TapeCharacter


def test_evaluator_blank_tape():
    input_text = "    "
    tape = parse_input_to_tape(input_text)
    for i in range(len(input_text)):
        assert tape[i] == TapeCharacter.BLANK

def test_evaluator_mixed_tape():
    input_text = "1 I -"
    tape = parse_input_to_tape(input_text)
    assert tape[0] == TapeCharacter.TALLY
    assert tape[1] == TapeCharacter.BLANK
    assert tape[2] == TapeCharacter.TALLY
    assert tape[3] == TapeCharacter.BLANK
    assert tape[4] == TapeCharacter.BLANK

def parse_input_to_tape(input_text: str):
    input_stream = InputStream(input_text)
    lexer = VarphiTapeLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = VarphiTapeParser(token_stream)
    tree = parser.tape()

    evaluator = VarphiTapeEvaluator()
    walker = ParseTreeWalker()
    walker.walk(evaluator, tree)
    
    return evaluator.tape