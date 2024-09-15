from VarphiTape.model import Tape, TapeCharacter

def test_tape_initialization():
    tape = Tape()
    assert tape[0] == TapeCharacter.BLANK
    assert tape[5] == TapeCharacter.BLANK
    assert tape[-3] == TapeCharacter.BLANK

def test_tape_set_and_get():
    tape = Tape()
    tape[0] = TapeCharacter.TALLY
    tape[1] = TapeCharacter.BLANK
    assert tape[0] == TapeCharacter.TALLY
    assert tape[1] == TapeCharacter.BLANK

def test_tape_representation():
    tape = Tape()
    tape[0] = TapeCharacter.TALLY
    tape[1] = TapeCharacter.TALLY
    tape[-1] = TapeCharacter.BLANK
    assert repr(tape) == "011"
