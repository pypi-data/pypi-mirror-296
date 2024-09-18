# flake8: noqa
# Generated from Varphi.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,5,63,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,
        4,1,4,1,5,1,5,4,5,34,8,5,11,5,12,5,35,1,6,1,6,3,6,40,8,6,1,7,1,7,
        3,7,44,8,7,1,8,1,8,1,8,1,8,5,8,50,8,8,10,8,12,8,53,9,8,1,8,1,8,1,
        9,4,9,58,8,9,11,9,12,9,59,1,9,1,9,0,0,10,1,0,3,0,5,0,7,0,9,0,11,
        1,13,2,15,3,17,4,19,5,1,0,8,2,0,76,76,108,108,2,0,82,82,114,114,
        2,0,81,81,113,113,4,0,49,49,73,73,105,105,124,124,5,0,48,48,66,66,
        79,79,98,98,111,111,4,0,48,57,65,90,95,95,97,122,2,0,10,10,13,13,
        3,0,9,10,13,13,32,32,62,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,
        17,1,0,0,0,0,19,1,0,0,0,1,21,1,0,0,0,3,23,1,0,0,0,5,25,1,0,0,0,7,
        27,1,0,0,0,9,29,1,0,0,0,11,31,1,0,0,0,13,39,1,0,0,0,15,43,1,0,0,
        0,17,45,1,0,0,0,19,57,1,0,0,0,21,22,7,0,0,0,22,2,1,0,0,0,23,24,7,
        1,0,0,24,4,1,0,0,0,25,26,7,2,0,0,26,6,1,0,0,0,27,28,7,3,0,0,28,8,
        1,0,0,0,29,30,7,4,0,0,30,10,1,0,0,0,31,33,3,5,2,0,32,34,7,5,0,0,
        33,32,1,0,0,0,34,35,1,0,0,0,35,33,1,0,0,0,35,36,1,0,0,0,36,12,1,
        0,0,0,37,40,3,7,3,0,38,40,3,9,4,0,39,37,1,0,0,0,39,38,1,0,0,0,40,
        14,1,0,0,0,41,44,3,1,0,0,42,44,3,3,1,0,43,41,1,0,0,0,43,42,1,0,0,
        0,44,16,1,0,0,0,45,46,5,47,0,0,46,47,5,47,0,0,47,51,1,0,0,0,48,50,
        8,6,0,0,49,48,1,0,0,0,50,53,1,0,0,0,51,49,1,0,0,0,51,52,1,0,0,0,
        52,54,1,0,0,0,53,51,1,0,0,0,54,55,6,8,0,0,55,18,1,0,0,0,56,58,7,
        7,0,0,57,56,1,0,0,0,58,59,1,0,0,0,59,57,1,0,0,0,59,60,1,0,0,0,60,
        61,1,0,0,0,61,62,6,9,0,0,62,20,1,0,0,0,6,0,35,39,43,51,59,1,6,0,
        0
    ]

class VarphiLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    STATE = 1
    SYMBOL = 2
    DIRECTION = 3
    COMMENT = 4
    WHITESPACE = 5

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
 ]

    symbolicNames = [ "<INVALID>",
            "STATE", "SYMBOL", "DIRECTION", "COMMENT", "WHITESPACE" ]

    ruleNames = [ "LEFT", "RIGHT", "Q", "TALLY", "BLANK", "STATE", "SYMBOL", 
                  "DIRECTION", "COMMENT", "WHITESPACE" ]

    grammarFileName = "Varphi.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


