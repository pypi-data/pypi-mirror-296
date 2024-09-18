from antlr4 import ParseTreeWalker, InputStream, CommonTokenStream
from varphi.antlr import VarphiLexer, VarphiParser, VarphiEvaluator
from varphi.model import TuringMachine
from varphitape.frontend import fileToTape


def fileToTuringMachine(programPath: str) -> TuringMachine:
    """
    Converts a Varphi language program file into a TuringMachine object.

    This function reads a program file, tokenizes the content using ANTLR,
    parses it into a parse tree, and uses a custom evaluator to create
    a TuringMachine instance with the parsed state.

    Args:
        programPath (str): The path to the Varphi language program file.

    Returns:
        TuringMachine: An instance of TuringMachine initialized with the
        state defined in the Varphi program.
    """
    with open(programPath, 'r') as file:
        program = file.read()

    input_stream = InputStream(program)
    lexer = VarphiLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = VarphiParser(token_stream)
    tree = parser.program()
    evaluator = VarphiEvaluator()
    walker = ParseTreeWalker()

    # Walk the tree using the implemented evaluator
    walker.walk(evaluator, tree)

    return TuringMachine(evaluator.initialState)


def execute(programPath: str, tapePath: str, outputPath: str) -> None:
    """
    Executes a Varphi language program with a given tape and writes the result
    to an output file.

    This function converts a Varphi program file to a TuringMachine object,
    reads a tape from the specified file, executes the Turing machine with the
    tape, and writes the resulting tape to the output file.

    Args:
        programPath (str): The path to the Varphi language program file.
        tapePath (str): The path to the file containing the tape.
        outputPath (str): The path to the file where the result tape will be
                          written.
    """
    turingMachine = fileToTuringMachine(programPath)
    tape = fileToTape(tapePath)

    turingMachine.execute(tape)

    with open(outputPath, "w+") as outputFile:
        outputFile.write(tape.__str__())
