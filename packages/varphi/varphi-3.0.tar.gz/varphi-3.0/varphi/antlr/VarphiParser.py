# Generated from Varphi.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,5,27,2,0,7,0,2,1,7,1,2,2,7,2,1,0,1,0,5,0,9,8,0,10,0,12,0,12,
        9,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,0,0,
        3,0,2,4,0,0,25,0,10,1,0,0,0,2,15,1,0,0,0,4,21,1,0,0,0,6,9,3,2,1,
        0,7,9,3,4,2,0,8,6,1,0,0,0,8,7,1,0,0,0,9,12,1,0,0,0,10,8,1,0,0,0,
        10,11,1,0,0,0,11,13,1,0,0,0,12,10,1,0,0,0,13,14,5,0,0,1,14,1,1,0,
        0,0,15,16,5,1,0,0,16,17,5,2,0,0,17,18,5,1,0,0,18,19,5,2,0,0,19,20,
        5,3,0,0,20,3,1,0,0,0,21,22,5,1,0,0,22,23,5,2,0,0,23,24,5,1,0,0,24,
        25,5,1,0,0,25,5,1,0,0,0,2,8,10
    ]

class VarphiParser ( Parser ):

    grammarFileName = "Varphi.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "STATE", "SYMBOL", "DIRECTION", "WHITESPACE", 
                      "NEWLINE" ]

    RULE_program = 0
    RULE_line = 1
    RULE_oracleLine = 2

    ruleNames =  [ "program", "line", "oracleLine" ]

    EOF = Token.EOF
    STATE=1
    SYMBOL=2
    DIRECTION=3
    WHITESPACE=4
    NEWLINE=5

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(VarphiParser.EOF, 0)

        def line(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VarphiParser.LineContext)
            else:
                return self.getTypedRuleContext(VarphiParser.LineContext,i)


        def oracleLine(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VarphiParser.OracleLineContext)
            else:
                return self.getTypedRuleContext(VarphiParser.OracleLineContext,i)


        def getRuleIndex(self):
            return VarphiParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)




    def program(self):

        localctx = VarphiParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1:
                self.state = 8
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,0,self._ctx)
                if la_ == 1:
                    self.state = 6
                    self.line()
                    pass

                elif la_ == 2:
                    self.state = 7
                    self.oracleLine()
                    pass


                self.state = 12
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 13
            self.match(VarphiParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LineContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STATE(self, i:int=None):
            if i is None:
                return self.getTokens(VarphiParser.STATE)
            else:
                return self.getToken(VarphiParser.STATE, i)

        def SYMBOL(self, i:int=None):
            if i is None:
                return self.getTokens(VarphiParser.SYMBOL)
            else:
                return self.getToken(VarphiParser.SYMBOL, i)

        def DIRECTION(self):
            return self.getToken(VarphiParser.DIRECTION, 0)

        def getRuleIndex(self):
            return VarphiParser.RULE_line

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLine" ):
                listener.enterLine(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLine" ):
                listener.exitLine(self)




    def line(self):

        localctx = VarphiParser.LineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_line)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 15
            self.match(VarphiParser.STATE)
            self.state = 16
            self.match(VarphiParser.SYMBOL)
            self.state = 17
            self.match(VarphiParser.STATE)
            self.state = 18
            self.match(VarphiParser.SYMBOL)
            self.state = 19
            self.match(VarphiParser.DIRECTION)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OracleLineContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STATE(self, i:int=None):
            if i is None:
                return self.getTokens(VarphiParser.STATE)
            else:
                return self.getToken(VarphiParser.STATE, i)

        def SYMBOL(self):
            return self.getToken(VarphiParser.SYMBOL, 0)

        def getRuleIndex(self):
            return VarphiParser.RULE_oracleLine

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOracleLine" ):
                listener.enterOracleLine(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOracleLine" ):
                listener.exitOracleLine(self)




    def oracleLine(self):

        localctx = VarphiParser.OracleLineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_oracleLine)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 21
            self.match(VarphiParser.STATE)
            self.state = 22
            self.match(VarphiParser.SYMBOL)
            self.state = 23
            self.match(VarphiParser.STATE)
            self.state = 24
            self.match(VarphiParser.STATE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





