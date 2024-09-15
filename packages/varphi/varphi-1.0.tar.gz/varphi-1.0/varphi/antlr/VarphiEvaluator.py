from .VarphiListener import VarphiListener
from .VarphiParser import VarphiParser
from varphi.model import State, Instruction, HeadDirection
from varphi_tape.model import TapeCharacter

# This class defines a complete listener for a parse tree produced by VarphiParser.
class VarphiEvaluator(VarphiListener):
    stateNameToObject: dict[str, State]
    initialState: State | None

    def __init__(self):
        self.stateNameToObject = {}
        self.initialState = None
        super().__init__()
    

    # Enter a parse tree produced by VarphiParser#program.
    def enterProgram(self, ctx:VarphiParser.ProgramContext):
        pass

    # Exit a parse tree produced by VarphiParser#program.
    def exitProgram(self, ctx:VarphiParser.ProgramContext):
        pass


    # Enter a parse tree produced by VarphiParser#line.
    def enterLine(self, ctx:VarphiParser.LineContext):
        ifState = str(ctx.STATE(0))
        ifCharacter = str(ctx.SYMBOL(0))
        thenState = str(ctx.STATE(1))
        thenCharacter = str(ctx.SYMBOL(1))
        thenDirection = str(ctx.DIRECTION)

        if ifState in self.stateNameToObject:
            ifStateObject = self.stateNameToObject[ifState]
        else:
            ifStateObject = State()
            self.stateNameToObject[ifState] = ifStateObject

            if self.initialState is None:
                self.initialState = ifStateObject
        
        ifCharacterObject = TapeCharacter.TALLY if ifCharacter == "I" else TapeCharacter.BLANK

        if thenState in self.stateNameToObject:
            thenStateObject = self.stateNameToObject[thenState]
        else:
            thenStateObject = State()
            self.stateNameToObject[thenState] = thenStateObject
        
        thenCharacterObject = TapeCharacter.TALLY if thenCharacter == 'I' else TapeCharacter.BLANK

        thenDirectionObject = HeadDirection.RIGHT if thenDirection == 'R' else HeadDirection.LEFT

        instruction = Instruction(thenStateObject, thenCharacterObject, thenDirectionObject)
        
        if ifCharacterObject == TapeCharacter.TALLY:
            ifStateObject.addOnTallyInstruction(instruction)
        else:
            ifStateObject.addOnBlankInstruction(instruction)


    # Exit a parse tree produced by VarphiParser#line.
    def exitLine(self, ctx:VarphiParser.LineContext):
        pass


    # Enter a parse tree produced by VarphiParser#oracleLine.
    def enterOracleLine(self, ctx:VarphiParser.OracleLineContext):
        pass

    # Exit a parse tree produced by VarphiParser#oracleLine.
    def exitOracleLine(self, ctx:VarphiParser.OracleLineContext):
        pass