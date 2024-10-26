from LexicAnalyzer import LexicAnalyzer
from LexicTreeBuilder import tree_graph, LexicTreeBuilder

PARSE = False
TREE = True
FILE = "testgroup/test_multi.py"

if PARSE:
    f = open(FILE, 'r')
    res, rem = LexicAnalyzer.parse_text(f.read())
    f.close()

if TREE:
    tree = LexicTreeBuilder('result.json')
    tree_graph(tree.root)

