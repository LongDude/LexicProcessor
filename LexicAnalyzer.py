import re, sys
import json
from enum import Enum

LOGGING =  True
SAVE_TO_FILE = True

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

class Subtypes:
    CommentSubTypes = _CommentSubTypes
    NumbersSubType = _NumbersSubType

class LexicAnalyzer(object):
    keyword = {
        "del",
        "global",
        "with",
        "as",
        "elif",
        "if",
        "yield",
        "assert",
        "else",
        "import",
        "pass",
        "break",
        "except",
        "raise",
        "class",
        "finally",
        "return",
        "continue",
        "for",
        "lambda",
        "try",
        "def",
        "from",
        "nonlocal",
        "while"
    }

    __first_filter:re.Pattern = re.compile(r"([']{3}[\s\S]*?[']{3})|([\"]{3}[\s\S]*?[\"]{3})|('{1}.*?'{1})|(\"{1}.*?\"{1})|([#].*?$)|((?<=['\"\])}a-z])\.)|(\s+)|([\[\]\{\}\(\),:;\\])|((?:\*{1,2}|/{1,2}|>{1,2}|<{1,2}|[%&|^!~])=?|={2}|[+-]?=|\b(?:and|or|not|in|is)\b)|((?:\_|[a-z])+[a-z0-9_]*)|([\w\.\+\-]+)", flags=re.M | re.S | re.X | re.I)
    __nums_processor: re.Pattern = re.compile(r"(^\.$)|(^[\+\-]$)|(0b[01]+)|(0o[0-7]+)|(0x[0-9a-f]+)|(^[0-9]+$)|(^[0-9]*\.[0-9]*(?:e[\+\-][0-9]+|e)?$)", flags=re.I)

    __multistring_cleaner: re.Pattern = re.compile(r"\s*\\\s")
    __multicomment_cleaner: re.Pattern = re.compile(r"\s{2,}")

    @staticmethod
    def __trim_multiline_strings(multiline_string) -> str: return re.sub(LexicAnalyzer.__multistring_cleaner, " ", multiline_string)

    @staticmethod
    def __trim_multiline_comments(multiline_comments) -> str: return re.sub(LexicAnalyzer.__multicomment_cleaner, " ", multiline_comments)

    @classmethod
    def __parse_regex(__class__, text):
        def tupl(m: re.Match, i, t: TokenType, st : Subtypes = None, wrapper = lambda x: x): return (wrapper(m.group(i)), m.span(i), t, st)

        result = []
        remainder = []
        for m in LexicAnalyzer.__first_filter.finditer(text):
                if   m.group(1)  is not None: result.append(tupl(m, 1, TokenType.COMMENT, wrapper=LexicAnalyzer.__trim_multiline_comments)) # Многострочные комментарии
                elif m.group(2)  is not None: result.append(tupl(m, 2, TokenType.COMMENT, wrapper=LexicAnalyzer.__trim_multiline_comments)) # Многострочные комментарии
                elif m.group(3)  is not None: result.append(tupl(m, 3, TokenType.STRING_LITERAL, wrapper=LexicAnalyzer.__trim_multiline_strings)) # Multiline string
                elif m.group(4)  is not None: result.append(tupl(m, 4, TokenType.STRING_LITERAL, wrapper=LexicAnalyzer.__trim_multiline_strings)) # Multiline string
                elif m.group(5)  is not None: result.append(tupl(m, 5, TokenType.COMMENT, Subtypes.CommentSubTypes.SINGLELINE))
                elif m.group(6)  is not None: result.append(tupl(m, 6, TokenType.DIVIDER))
                elif m.group(7)  is not None: pass # Trim whitespaces
                elif m.group(8)  is not None: result.append(tupl(m, 8, TokenType.DIVIDER))
                elif m.group(9)  is not None: result.append(tupl(m, 9, TokenType.OPERATOR))
                elif m.group(10) is not None: result.append(tupl(m, 10, TokenType.KEYWORD if m.group(10) in LexicAnalyzer.keyword else TokenType.IDENTIFIER))
                elif m.group(11) is not None:
                    # mmmhmm float
                    for sub_m in LexicAnalyzer.__nums_processor.finditer(m.group(11)):
                        if   sub_m.group(1) is not None: result.append(tupl(sub_m, 1, TokenType.DIVIDER))
                        elif sub_m.group(2) is not None: result.append(tupl(sub_m, 2, TokenType.OPERATOR))
                        elif sub_m.group(3) is not None: result.append(tupl(sub_m, 3, TokenType.NUMBER_LITERAL, Subtypes.NumbersSubType.BINARY))
                        elif sub_m.group(4) is not None: result.append(tupl(sub_m, 4, TokenType.NUMBER_LITERAL, Subtypes.NumbersSubType.OCTAL))
                        elif sub_m.group(5) is not None: result.append(tupl(sub_m, 5, TokenType.NUMBER_LITERAL, Subtypes.NumbersSubType.HEXADIMECIAL))
                        elif sub_m.group(6) is not None: result.append(tupl(sub_m, 6, TokenType.NUMBER_LITERAL, Subtypes.NumbersSubType.INTEGER))
                        elif sub_m.group(7) is not None: result.append(tupl(sub_m, 7, TokenType.NUMBER_LITERAL, Subtypes.NumbersSubType.FLOAT))
                        elif sub_m.group(8) is not None:
                            remainder.append((sub_m.group(8), sub_m.span(8)[0] + m.span(11)[0], sub_m.span(8)[1] + m.span(11)[0]))
                        else: print(f"How did you get here? [{sub_m.string}]")
                else:
                    # This is the point of no return
                    print(f"Error: no match:{m.string}")

        return result, remainder

    def parse_text(text):
        ''' Мастер по поэтапной прогонке текста '''
        if SAVE_TO_FILE:
            resultFile = open("result"  + ".json", "w")

        if LOGGING:
            from datetime import datetime
            from pathlib import Path
            path = Path("./log/")
            if not path.exists():
                path.mkdir(parents=True)

            tempfile1 = open("log/log" + str(datetime.now()), 'a+')
        
        res, rem = LexicAnalyzer.__parse_regex(text)
        if LOGGING:
            tempfile1.write("== Iter 1 res\n ==")
            tempfile1.write("\n".join(list(map(lambda x: str(x), res))))
            if rem:
                tempfile1.write("== REMAINDER ==")

        if SAVE_TO_FILE:
            resultFile.write(json.dumps(res))
            resultFile.close()

        if LOGGING:
            tempfile1.close()

        return res, rem

if __name__ == "__main__":
    testfile = open("test.txt", 'r')
    res, rem = LexicAnalyzer.parse_text(testfile.read())
    
    print("=== RESULT ===", *res, sep="\n")

    if rem:
        print("=== REMAINDER ===", *rem, sep="\n")

    testfile.close()