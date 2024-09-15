from tempfile import NamedTemporaryFile

from VarphiTape.model import TapeCharacter
from VarphiTape.frontend import fileToTape


def test_file_to_tape():
    with NamedTemporaryFile('w+', delete=False) as temp_file:
        temp_file.write("1 I -")
        temp_file.flush()
        temp_file.seek(0)
        
        tape = fileToTape(temp_file.name)
        
    assert tape[0] == TapeCharacter.TALLY
    assert tape[1] == TapeCharacter.BLANK
    assert tape[2] == TapeCharacter.TALLY
    assert tape[3] == TapeCharacter.BLANK
    assert tape[4] == TapeCharacter.BLANK
