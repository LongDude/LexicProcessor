from LexicAnalyzer import LexicAnalyzer
from LexicTreeBuilder import tree_graph, LexicTreeBuilder
from LexicInterpretator import LexicInterpretator

PARSE = True
TREE = True
INTERP = True
LOGGING =  False
FILE = "testgroup/factorial.py"

if PARSE:
    f = open(FILE, 'r')
    res, rem = LexicAnalyzer.parse_text(f.read())
    f.close()

if TREE:
    tree = LexicTreeBuilder('result.json')
    if INTERP:
        intrp = LexicInterpretator(tree.root)
        intrp.exec()
    tree_graph(tree.root)
    