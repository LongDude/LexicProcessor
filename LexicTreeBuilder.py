import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import graphviz_layout
import json
from LexicTokenTypes import *

SHOW_DIAP = False
PSEUDOELEMENT = True


class TokenReader(object):
    __tokens : list = []
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
    def __init__(self, lbl, diap=[0,0], t_type:TokenType=None, t_subtype:Subtypes=None):
        self.label = lbl
        self.__diap = diap
        self.childs = []
        self.parent = None
        self.t_type = t_type
        self.t_subtype = t_subtype

    def create_child_named(self, lbl: str, meta_subtype:Subtypes.MetaSubType = Subtypes.MetaSubType.ABSTRACT):
        child = TreeNode(lbl, t_type=TokenType.META, t_subtype=meta_subtype)
        self.childs.append(child)
        child.parent = self
        return child

    def create_child_auto(self, token:list):
        child = TreeNode(token[0], token[2], token[3], token[4])
        self.childs.append(child)
        child.parent = self
        return child
    
    def add_child(self, child):
        child.parent = self
        self.childs.append(child)

    @property
    def diap(self): return self.__diap

class LexicTreeBuilder(object):
    root : TreeNode
    tokens : list

    def __init__(self, f_name: str):
        self.tokens = TokenReader(f_name).tokens
        self.root: TreeNode = TreeNode("ROOT", [self.tokens[0][2][0], self.tokens[-1][2][1]])
        self.build(self.root)

    def build(self, root: TreeNode, p=0):
        def test_token_val(idx, value):
            if self.tokens[p][0] != value: raise ValueError("Token Error", tokens[p])
            return p + 1
        
        def test_token_type(idx, type):
            if self.tokens[p][3] != type: raise ValueError("Token Error", tokens[p])
            return p + 1

        # Oh shit

        tokens = self.tokens
        
        identation = tokens[p][1]
        while p < len(tokens):
            if tokens[p][1] < identation: # If current body block ended
                if tokens[p][3] == TokenType.ENTERS:
                    p += 1
                    continue
                return p
            
            match tokens[p][3]:
                case TokenType.KEYWORD:
                    match tokens[p][0]:
                        case "def":
                            def_root = root.create_child_auto(tokens[p]) # Function root
                            p += 1

                            def_root.create_child_auto(tokens[p]) # Function identifier
                            p += 1

                            # Bracket block
                            args_root = def_root.create_child_named('()', Subtypes.MetaSubType.ARGS)
                            p = self.parse_args(args_root, p)

                            p = test_token_val(p, ":")
                            if tokens[p][3] == TokenType.ENTERS: p += 1

                            # Recursive build local tree from body block
                            # Inside block can (and would) be parsed as programm itself
                            if PSEUDOELEMENT:
                                body_root = def_root.create_child_named('BODY', Subtypes.MetaSubType.BODY)
                            else:
                                body_root = def_root
                            p = self.build(body_root, p)

                        case 'for':
                            # 1. FOR keyword
                            for_root = root.create_child_auto(tokens[p])
                            p += 1

                            # 2. List of identifiers
                            while tokens[p][3] == TokenType.IDENTIFIER:
                                for_root.create_child_auto(tokens[p])
                                p += 1

                                if tokens[p][0] == ',': p += 1
                            
                            # 3. Keyword 'in'
                            if tokens[p][0] == "in":
                                for_root.create_child_auto(tokens[p])
                                p += 1
                            else:
                                raise ValueError("Token Error", tokens[p])

                            # 4. Generic Collection (upcast to rvalue for simplicity)
                            p = self.parse_expr(for_root, p)

                            # 5. Finisher
                            p = test_token_val(p, ":")
                            if tokens[p][3] == TokenType.ENTERS: p += 1

                            # 6. Inner block
                            if PSEUDOELEMENT:
                                body_root = for_root.create_child_named('BODY', Subtypes.MetaSubType.BODY)
                            else:
                                body_root = for_root
                            p = self.build(body_root, p)

                            if p >= len(tokens): return p

                            # 7. Else keyword
                            if tokens[p][3] == TokenType.KEYWORD and tokens[p][0] == "else":
                                else_block = for_root.create_child_auto(tokens[p])
                                p += 1

                                p = test_token_val(p, ":")
                                if tokens[p][3] == TokenType.ENTERS: p += 1
                                p = self.build(else_block, p)

                        case 'if':
                            # 1. if keyword
                            if_root = root.create_child_auto(tokens[p])
                            p += 1

                            # 2. Rvalue (condition block)
                            p = self.parse_expr(if_root, p)

                            # 3. deco
                            p = test_token_val(p, ":")
                            if tokens[p][3] == TokenType.ENTERS: p += 1

                            # 4. Function body
                            if PSEUDOELEMENT:
                                body_root = if_root.create_child_named('BODY', Subtypes.MetaSubType.BODY)
                            else:
                                body_root = if_root
                            p = self.build(body_root, p)

                            if p >= len(tokens): return p

                            # 5. Elif block(s)
                            while tokens[p][3] == TokenType.KEYWORD and tokens[p][0] == "elif":
                                elif_root = if_root.create_child_auto(tokens[p])
                                p += 1
                                p = self.parse_expr(elif_root, p)
                                p = test_token_val(p, ":")
                                if tokens[p][3] == TokenType.ENTERS: p += 1
                                p = self.build(elif_root, p)

                                if p >= len(tokens): return p


                            # 6. Else block
                            if tokens[p][3] == TokenType.KEYWORD and tokens[p][0] == "else":
                                else_root = if_root.create_child_auto(tokens[p])
                                p += 1
                                p = test_token_val(p, ":")
                                if tokens[p][3] == TokenType.ENTERS: p += 1
                                p = self.build(else_root, p)


                        case 'while':
                            while_root = root.create_child_auto(tokens[p])
                            p += 1

                            p = self.parse_expr(while_root, p)
                            
                            p = test_token_val(p, ":")
                            if tokens[p][3] == TokenType.ENTERS: p += 1
                            body_root = while_root.create_child_named("BODY", Subtypes.MetaSubType.BODY)
                            p = self.build(while_root)
                                                                            
                        case 'return':
                            return_root = root.create_child_auto(tokens[p])
                            p += 1

                            while tokens[p][3] == TokenType.IDENTIFIER:
                                return_root.create_child_auto(tokens[p])
                                p += 1
                                if tokens[p][0] == ",": 
                                    p += 1
                                    if tokens[p][3] == TokenType.ENTERS: 
                                        p += 1

                        case _: 
                            p += 1
                case TokenType.IDENTIFIER:
                    p = self.parse_expr(root, p)
                case _: 
                    p += 1
        return p

    def parse_args(self, root: TreeNode, p):
        p += 1
        while self.tokens[p][0] != ")":
            identificator = None
            defVal = None

            if identificator is None: identificator = root.create_child_auto(self.tokens[p])
            else: raise ValueError('Unexpected Token:', self.tokens[p])
            p += 1

            # Using if cos conditions can be chained
            if self.tokens[p][0] == ':': # type block
                p += 1
                p = self.parse_type(identificator, p)
                            
            if self.tokens[p][0] == '=':
                p += 1
                defVal = identificator.create_child_named('DEFAULT', Subtypes.MetaSubType.DEFAULT)
                p = self.parse_expr(defVal, p)

            if self.tokens[p][0] == ',' or self.tokens[p][3] == TokenType.ENTERS:
                p += 1
            
        return p + 1

    def parse_type(self, identificator: TreeNode, p):
        # PSEUDOELEMENT
        if self.tokens[p][3] == TokenType.IDENTIFIER:
            identificator.create_child_auto(self.tokens[p])
            p += 1
        elif self.tokens[p][0] == '[':
            types_stack = [identificator.create_child_auto(self.tokens[p])]
            p += 1
            while len(types_stack) > 0:
                if self.tokens[p][0] == '[':
                    types_stack.append(types_stack[-1].create_child_auto(self.tokens[p]))
                elif self.tokens[p][0] == ']':
                    types_stack[-1].set_diap(r=self.tokens[p][2][1])
                    types_stack.pop()
                else:
                    types_stack[-1].create_child_auto(self.tokens[p])
                    p += 1

        else: raise ValueError('Unexpected Token:', self.tokens[p])
        return p # Next element after type block

    def parse_expr(self, container: TreeNode, p) -> int:
        elements_list = []
        tokens = self.tokens # small alias
        # Parse string (until break)
        await_value = True
        while p < len(self.tokens):
            match tokens[p][3]: 
                case TokenType.IDENTIFIER:
                    elements_list.append(TreeNode(tokens[p][0], tokens[p][2], tokens[p][3], tokens[p][4]))
                    p += 1
                    p = self.parse_identificator(elements_list[-1], p)
                    await_value = False
                case TokenType.DIVIDER:
                    match tokens[p][0]:
                        case ":": # Expression finished
                            for i in elements_list:
                                container.add_child(i)
                            return p
                        case ",":
                            await_value = True
                            p += 1

                        case "[": # List (identificators already processed indexes)
                            subexpr = container.create_child_named("[]", Subtypes.MetaSubType.GROUP)
                            p += 1
                            p = self.parse_expr(subexpr, p)
                            p += 1

                        case "(":
                            subexpr = container.create_child_named("()", Subtypes.MetaSubType.LIST)
                            p += 1
                            p = self.parse_expr(subexpr, p)

                        case "]" | ")": # End of list
                            for i in elements_list:
                                container.add_child(i)
                            return p

                case TokenType.ENTERS:
                    if await_value: p += 1
                    else:
                        for el in elements_list:
                            container.add_child(el)
                        return p + 1

                case TokenType.NUMBER_LITERAL | TokenType.STRING_LITERAL:
                    elements_list.append(TreeNode(tokens[p][0], tokens[p][2], tokens[p][3], tokens[p][4]))
                    p += 1
                case TokenType.OPERATOR:
                    operator_root = container.create_child_auto(tokens[p])
                    p += 1
                    l = operator_root.create_child_named('lval', Subtypes.MetaSubType.LVAL)
                    for i in elements_list:
                        l.add_child(i)
                        elements_list = []
                    container = operator_root
                case _:
                    p += 1
        return p
    
    def parse_identificator(self, ident_root: TreeNode, p):
        ''' Identificator can be function call, class or lvalue'''
        while p < len(self.tokens):
            if self.tokens[p][0] == ".":
                p += 1
                if self.tokens[p][3] == TokenType.ENTERS: p += 1
                if self.tokens[p][3] != TokenType.IDENTIFIER:
                    raise ValueError("Token Error", self.tokens[p])
                ident_root = ident_root.create_child_auto(self.tokens[p])
                p += 1
            elif self.tokens[p][0] == "(":
                args = ident_root.create_child_named("()", Subtypes.MetaSubType.FUNC_PARAMS)
                p += 1
                p = self.parse_expr(args, p)
                p += 1
            elif self.tokens[p][0] == "[":
                p = self.parse_index(ident_root, p)
            else:
                return p
            

    def parse_index(self, ident_root: TreeNode, p):
        container = ident_root.create_child_named("[]", Subtypes.MetaSubType.INDEX)
        p += 1
        # Extreme case: [::]                
        if self.tokens[p][0] != ":": # Blanks for indexation
            p = self.parse_expr(container, p)

        if self.tokens[p][0] == ":": p += 1

        if self.tokens[p][0] != ":" and self.tokens[p][0] != "]": # Blanks for indexation
            p = self.parse_expr(container, p)

        if self.tokens[p][0] == ":": p += 1

        if self.tokens[p][0] != ":" and self.tokens[p][0] != "]": # Blanks for indexation
            p = self.parse_expr(container, p)

        if self.tokens[p][0] != "]":
            raise ValueError("Token Error", self.tokens[p])
        p += 1
        return p

def tree_dfs(node: TreeNode, graph: nx.Graph, labels:dict, idx=0):
    if SHOW_DIAP:
        if node.diap:
            labels[idx] = node.label + '\n' + str(node.diap)
        else:
            labels[idx] = node.label
    else:
        labels[idx] = node.label

    if node.t_type:     labels[idx] += '\n' + node.t_type.name
    if node.t_subtype:  labels[idx] += '\n' + node.t_subtype.name
    graph.add_node(idx)
    curr_idx = idx
    idx += 1
    for subnode in node.childs:
        n_idx = tree_dfs(subnode, graph, labels, idx)
        graph.add_edge(curr_idx, idx)
        idx = n_idx
    return idx

def tree_graph(node: TreeNode):
    G = nx.Graph()
    lbls = {}
    tree_dfs(node, G, lbls)

    pos = graphviz_layout(G, 'dot')
    nx.draw(G, pos, node_size=1300, node_color="lightgray")
    nx.draw_networkx_labels(G, pos, lbls, font_size=8)
    plt.show()


if __name__ == "__main__":
    o = LexicTreeBuilder('result.json')
    tree_graph(o.root)
