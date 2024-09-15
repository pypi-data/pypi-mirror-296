# Generated from VarphiTape.g4 by ANTLR 4.13.2
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
        4,1,2,11,2,0,7,0,1,0,5,0,4,8,0,10,0,12,0,7,9,0,1,0,1,0,1,0,0,0,1,
        0,0,1,1,0,1,2,10,0,5,1,0,0,0,2,4,7,0,0,0,3,2,1,0,0,0,4,7,1,0,0,0,
        5,3,1,0,0,0,5,6,1,0,0,0,6,8,1,0,0,0,7,5,1,0,0,0,8,9,5,0,0,1,9,1,
        1,0,0,0,1,5
    ]

class VarphiTapeParser ( Parser ):

    grammarFileName = "VarphiTape.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "TALLY", "BLANK" ]

    RULE_tape = 0

    ruleNames =  [ "tape" ]

    EOF = Token.EOF
    TALLY=1
    BLANK=2

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class TapeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(VarphiTapeParser.EOF, 0)

        def TALLY(self, i:int=None):
            if i is None:
                return self.getTokens(VarphiTapeParser.TALLY)
            else:
                return self.getToken(VarphiTapeParser.TALLY, i)

        def BLANK(self, i:int=None):
            if i is None:
                return self.getTokens(VarphiTapeParser.BLANK)
            else:
                return self.getToken(VarphiTapeParser.BLANK, i)

        def getRuleIndex(self):
            return VarphiTapeParser.RULE_tape

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTape" ):
                listener.enterTape(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTape" ):
                listener.exitTape(self)




    def tape(self):

        localctx = VarphiTapeParser.TapeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_tape)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 5
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1 or _la==2:
                self.state = 2
                _la = self._input.LA(1)
                if not(_la==1 or _la==2):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 7
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 8
            self.match(VarphiTapeParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





