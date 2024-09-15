from varphi_tape.model import TapeCharacter

def test_blank_character():
    assert TapeCharacter.BLANK == TapeCharacter(0)

def test_tally_character():
    assert TapeCharacter.TALLY == TapeCharacter(1)