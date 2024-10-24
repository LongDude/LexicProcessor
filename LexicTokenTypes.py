from enum import Enum

def token_decoder(n1, n2):
    t1 = TokenType(n1)
    match t1:
        case TokenType.COMMENT: t2 = Subtypes.CommentSubTypes(n2)
        case TokenType.NUMBER_LITERAL: t2 = Subtypes.NumbersSubType(n2)
        case _: t2 = None
    return t1, t2

class TokenType(int, Enum):
    COMMENT = 0
    STRING_LITERAL = 1
    NUMBER_LITERAL = 2
    DIVIDER = 3
    OPERATOR = 4
    KEYWORD = 5
    IDENTIFIER = 6

class _CommentSubTypes(int, Enum):
    SINGLELINE = 0
    MULTILINE = 1

class _NumbersSubType(int, Enum):
    INTEGER = 0
    FLOAT = 1
    BINARY = 2
    OCTAL = 3
    HEXADIMECIAL = 4

class _BracketsType(int, Enum):
    OPEN_PARENTHESES = 0
    CLOSE_PARENTHESES = 1
    OPEN_BRACKETS = 2
    CLOSE_BRACKETS = 3
    OPEN_SQBRAKETS = 4
    CLOSE_SQBRACKETS = 5

class Subtypes:
    CommentSubTypes = _CommentSubTypes
    NumbersSubType = _NumbersSubType
    BracketsSubType = _BracketsType
