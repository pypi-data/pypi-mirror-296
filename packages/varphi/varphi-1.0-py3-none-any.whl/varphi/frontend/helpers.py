from antlr4 import *
from varphi.antlr import VarphiLexer, VarphiParser, VarphiEvaluator
from varphi.model import TuringMachine
from varphi_tape.frontend import fileToTape


def fileToTuringMachine(programPath: str) -> TuringMachine:
    # Open and read the program file
    with open(programPath, 'r') as file:
        program = file.read()
    
    # Create an ANTLR input stream from the program string
    input_stream = InputStream(program)
    
    # Initialize the lexer with the input stream
    lexer = VarphiLexer(input_stream)
    
    # Tokenize the input
    token_stream = CommonTokenStream(lexer)
    
    # Initialize the parser with the token stream
    parser = VarphiParser(token_stream)
    
    # Parse the input starting with the root rule (adjust 'startRule' to match your grammar)
    tree = parser.program()  # Adjust to your starting rule
    
    # Initialize your custom listener
    evaluator = VarphiEvaluator()
    
    # Create a parse tree walker
    walker = ParseTreeWalker()
    
    # Walk the tree using your custom listener
    walker.walk(evaluator, tree)

    return TuringMachine(evaluator.initialState)

def execute(programPath: str, tapePath: str, outputPath: str) -> None:
    turingMachine = fileToTuringMachine(programPath)
    tape = fileToTape(tapePath)

    turingMachine.execute(tape)

    with open(outputPath, "w+") as outputFile:
        outputFile.write(tape.__str__())