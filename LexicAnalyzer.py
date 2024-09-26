import re, sys

LOGGING =  True

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
    delimeters = "[\\[\\]().\\,:;{}\\x60@'\"]"
    ops = "`(?:[/*<>]{1,2}|[&%^+\\-\\\\|])={0,1}|[!=]{0,1}=|and|or|not|in|is`gms"

    __first_filter:re.Pattern = re.compile(r"('{3}[\s\S]*?'{3})|(\"{3}[\s\S]*?\"{3})|('{1}.*?'{1})|(\"{1}.*?\"{1})|([#].*?$)|(\s+)|(\S*)", flags=re.M | re.S)
    __delims_filter: re.Pattern = re.compile(r"((?:\*{1,2}|/{1,2}|>{1,2}|<{1,2}|[%&|^!~])=?|={2}|[+-]?=|\b(?:and|or|not|in|is)\b)|([()\[\]{},:;\\@])|(^[a-z]+$)|([a-z0-9+\-._]+)", flags=re.I)

    @staticmethod
    def safe_add(dictionary, classname, item, span):
        if item not in dictionary[classname]:
            dictionary[classname][item] = []
        dictionary[classname][item].append(span)

    @staticmethod
    def move_span(span, delta):
        return (span[0] + delta, span[1] + delta)

    @classmethod
    def first_iteration(__class__, result, text):
        remainder = []
        for m in LexicAnalyzer.__first_filter.finditer(text):
            for i in [0, 1, 2, 3, 4, 6]:
                if m.group(i+1) is None:
                    continue
                if i == 0 or i == 1 or i == 4:
                    result["Комментарии"].append((m.groups()[i], m.span(i+1)))
                elif i == 2 or i == 3:
                    result["Литеры"].append((m.groups()[i], m.span(i+1)))
                elif i == 6:
                    remainder.append((m.groups()[i], m.span(i+1)[0]))
        return remainder

    @classmethod
    def second_iteration(__class__, result, text_array):
        ''' Очищаем от разделителей, операций и точки-разделителя '''
        remainder = []
        for line, delta in text_array:
            for m in LexicAnalyzer.__delims_filter.finditer(line):
                if   m.group(1) is not None: LexicAnalyzer.safe_add(result, "Операторы:",   m.group(1), __class__.move_span(m.span(1), delta))
                elif m.group(2) is not None: LexicAnalyzer.safe_add(result, "Разделители:", m.group(2), __class__.move_span(m.span(2), delta))
                elif m.group(3) is not None:
                    word:str = m.group(3)
                    if word.lower() in LexicAnalyzer.keyword:
                        LexicAnalyzer.safe_add(result, "Ключевые слова:", word, __class__.move_span(m.span(3), delta))
                    else:
                        LexicAnalyzer.safe_add(result, "Идентификаторы:", word, __class__.move_span(m.span(3), delta))
                else:
                    remainder.append((m.group(4), m.span(4)[0] + delta))
        return remainder

    def filtare_text(text):
        ''' Мастер по поэтапной прогонке текста '''
        result = {"Комментарии": [], "Литеры": [], "Разделители:": {}, "Операторы:": {}, "Ключевые слова:": {}, "Идентификаторы:": {}}

        if LOGGING:
            from datetime import datetime
            tempfile1 = open("log", 'w+')
        
        rem = LexicAnalyzer.first_iteration(result, text)
        if LOGGING:
            tempfile1.write(str(datetime.now()) + " " + "Iter 1 res")
            tempfile1.write("\n".join(list(map(lambda x: x[0], rem))))

        rem = LexicAnalyzer.second_iteration(result, rem)
        if LOGGING:
            tempfile1.write(str(datetime.now()) +  " " + "Iter 2 res")
            tempfile1.write("\n".join(list(map(lambda x: x[0], rem))))

        if LOGGING:
            tempfile1.close()
        return result    

if __name__ == "__main__":
    testfile = open("test.txt", 'r')
    res =  LexicAnalyzer.filtare_text(testfile.read())
    testfile.close()
    print(res)
