from LexicAnalyzer import LexicAnalyzer
from LexicTreeBuilder import tree_graph, LexicTreeBuilder

PARSE = True
TREE = True
FILE = "testgroup/fibbonachi_seq.py"

if PARSE:
    f = open(FILE, 'r')
    res, rem = LexicAnalyzer.parse_text(f.read())
    f.close()

if TREE:
    tree = LexicTreeBuilder('result.json')
    tree_graph(tree)

