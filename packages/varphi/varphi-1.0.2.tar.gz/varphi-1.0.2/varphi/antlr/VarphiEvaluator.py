from .VarphiListener import VarphiListener
from .VarphiParser import VarphiParser
from varphi.model import State, Instruction, HeadDirection
from varphitape.model import TapeCharacter

TALLY_CHARACTERS = {'1', 'I', 'i', '|'}
BLANK_CHARACTERS = {'0', 'O', 'o', 'b', 'B'}
LEFT_CHARACTERS = {'l', 'L'}
RIGHT_CHARACTERS = {'r', 'R'}


class VarphiEvaluator(VarphiListener):
    """
    This class defines a complete Evaluator for a parse tree produced by
    VarphiParser.
    It processes parse tree nodes to build up an initial state for the Turing
    machine.
    """
    stateNameToObject: dict[str, State]
    initialState: State | None

    def __init__(self):
        """
        Initializes the VarphiEvaluator.
        Sets up a mapping of state names to State objects and initializes
        the initial state to None.
        """
        self.stateNameToObject = {}
        self.initialState = None
        super().__init__()

    def enterLine(self, ctx: VarphiParser.LineContext) -> None:
        """
        Enter a parse tree produced by VarphiParser#line.
        Processes the parse tree nodes to extract state transitions and
        instructions.

        Args:
            - ctx (VarphiParser.LineContext): The context for the parse tree
              node.
        """
        ifState = str(ctx.STATE(0).getText())
        ifCharacter = str(ctx.SYMBOL(0).getText())
        thenState = str(ctx.STATE(1).getText())
        thenCharacter = str(ctx.SYMBOL(1).getText())
        thenDirection = str(ctx.DIRECTION().getText())

        if ifState in self.stateNameToObject:
            ifStateObject = self.stateNameToObject[ifState]
        else:
            ifStateObject = State()
            self.stateNameToObject[ifState] = ifStateObject

            if self.initialState is None:
                self.initialState = ifStateObject

        if ifCharacter in TALLY_CHARACTERS:
            ifCharacterObject = TapeCharacter.TALLY
        else:
            ifCharacterObject = TapeCharacter.BLANK

        if thenState in self.stateNameToObject:
            thenStateObject = self.stateNameToObject[thenState]
        else:
            thenStateObject = State()
            self.stateNameToObject[thenState] = thenStateObject

        if thenCharacter in TALLY_CHARACTERS:
            thenCharacterObject = TapeCharacter.TALLY
        else:
            thenCharacterObject = TapeCharacter.BLANK

        if thenDirection in RIGHT_CHARACTERS:
            thenDirectionObject = HeadDirection.RIGHT
        else:
            thenDirectionObject = HeadDirection.LEFT

        instruction = Instruction(thenStateObject,
                                  thenCharacterObject,
                                  thenDirectionObject)

        if ifCharacterObject == TapeCharacter.TALLY:
            ifStateObject.addOnTallyInstruction(instruction)
        else:
            ifStateObject.addOnBlankInstruction(instruction)
