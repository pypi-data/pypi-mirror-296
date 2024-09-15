from antlr4 import *
from VarphiTape.antlr import VarphiTapeLexer, VarphiTapeParser, VarphiTapeEvaluator
from VarphiTape.model import Tape


def fileToTape(tapeFilePath: str) -> Tape:
    """
    Parses a tape file and returns the corresponding Turing machine tape.
    
    Args:
    - tapeFilePath (str): Path to the file containing the tape representation.
    
    Returns:
    - Tape: The parsed tape model.
    """
    # Open and read the program file
    with open(tapeFilePath, 'r') as file:
        program = file.read()

    # Create an ANTLR input stream from the program string
    input_stream = InputStream(program)
    
    # Initialize the lexer with the input stream
    lexer = VarphiTapeLexer(input_stream)
    
    # Tokenize the input
    token_stream = CommonTokenStream(lexer)
    
    # Initialize the parser with the token stream
    parser = VarphiTapeParser(token_stream)
    
    # Parse the input starting with the root rule
    tree = parser.tape()
    
    # Initialize the implemented evaluator
    evaluator = VarphiTapeEvaluator()
    
    # Create a parse tree walker
    walker = ParseTreeWalker()
    
    # Walk the tree using the evaluator
    walker.walk(evaluator, tree)
    
    return evaluator.tape
