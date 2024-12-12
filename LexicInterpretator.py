from LexicTreeBuilder import TreeNode
from LexicTokenTypes import *

class LexicInterpretator(object):
    _root: TreeNode # Узел
    _namespace_table = {} # 
    
    _inter_stack = []

    
    def __init__(self, tree_root: TreeNode):
        pass