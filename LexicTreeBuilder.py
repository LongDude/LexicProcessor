import networkx as nx
import matplotlib.pyplot as plt
import json
from LexicTokenTypes import *

class TokenReader(object):
    def __init__(self):
        self.tokens = []

    def __init__(self, f_name):
        self.tokens = f_name

    @property
    def tokens(self): return self.__tokens
    
    @tokens.setter
    def tokens(self, f_name):
        with open(f_name, "r") as f:
            self.__tokens = json.load(f)
            for element in self.__tokens:
                p = token_decoder(element[3], element[4])
                element[3] = p[0]
                element[4] = p[1]
        return self.__tokens

class TreeNode(object):
    def __init__(self, lbl, diap=(0,0)):
        self.label = lbl
        self.diap = diap
        self.childs = []

    def create_child(self, lbl, diap=[0,0]):
        child = TreeNode(lbl, diap)
        self.childs.append(child)
        return child

    def create_child(self, token:list):
        child = TreeNode(token[0], token[2])
        self.childs.append(child)
        return child

    def get_lbl(self): return self.lbl
    def get_child(self): return self.childs

class LexicTreeBuilder(object):
    root : TreeNode
    tokens : list

    def __init__(self, f_name: str):
        self.tokens = TokenReader(f_name)
        self.root: TreeNode = TreeNode("surrogate root", p=None)
        LexicTreeBuilder.build(self.root, tokens, 0, len(tokens))

    def build(root, str:int, end:int):
        # Oh shit
        tokens = self.tokens
        p = str
        while p < end:
            match tokens[p][3]:
                case TokenType.KEYWORD:
                    match tokens[p][0]:
                        case "def":
                            # Generating function tree
                            def_root = self.root.create_child(tokens[p])
                            p += 1

                            # Simple checks
                            if tokens[p][3] != TokenType.IDENTIFIER:
                                raise ValueError('Unexpected Token:', tokens[p])
                            sub_root.create_child(tokens[p])
                            p += 1

                            if tokens[p][0] != '(':
                                raise ValueError('Unexpected Token:', tokens[p])
                            larg = p+1
                            while tokens[p] != ')':
                                p += 1
                            args_root = sub_root.create_child('()', [tokens[larg][2][0], tokens[p][2][1]])
                            
                            p += 1
                            self.function_args(args_root, larg, p) # Parse function arguments

                            # Function header end
                            if tokens[p][0] != ':':
                                raise ValueError('Unexpected Token:', tokens[p])
                            p += 1

                            # Fast-parse function block
                            # Anything inside function can (and would) be parsed as programm itself
                            body_start, body_end = self.parse_fblock(p)
                            body_root = sub_root.create_child('body', [tokens[body_start][2][0], tokens[body_end][2][1] if body_end < end else tokens[-1][2][1]])
                            
                            self.build(body_root, body_start, p)   
                        case 'for':
                            pass

                        case 'if':
                            pass
                        
                        case 'while':
                            pass

    def parse_fblock(p):
        ident = tokens[p][1]
        body_start = p
        while tokens[p][1] >= ident and p < end: p += 1 # Search function end
        return body_start, p

    def function_args(root: TreeNode, str, end):
        pass



    @property
    def root(self):
        return self.__tree_root




class LexitTreeDisplay(object):
    def __init__(self, root=TreeNode):
        pass

o = TokenReader('result.json')

G = nx.Graph()
G.add_edge(1,2)
G.add_edge(1,3)
nx.draw(G, with_labels=True)
plt.show()
