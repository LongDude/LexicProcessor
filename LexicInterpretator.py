from LexicTreeBuilder import TreeNode
from LexicTokenTypes import *

VERBOUSE = True

class LexicInterpretator(object):
    _root: TreeNode # Узел
    _stack = []
    _rec_stack = []
    _rec_counter = 0

    def __init__(self, tree_root: TreeNode):
        self._root = tree_root
        self._stack = []
        self._rec_stack = [0]
        self._rec_counter = 0

    def exec(self):
        '''
            По умолчанию выполняет общий код интерпретируемой программы
        '''
        self._stack.append(dict()) # Создаем локальный стек
        self._rec_stack.append(self._rec_counter)
        self.__parse_node(self._root)
        self._rec_stack.pop()
        self._stack.pop()


    def __parse_node(self, node:TreeNode):
        '''
            Спускаемся в глубину, каждый вызов функции пораждает новую запись в стеке
            Поиск переменной вверх по стеку. При перепределении в стеке появляется новая запись
        '''
        rec_level = self._rec_counter # Запоминаем текущий уровень вызова
        # Если внутри блоков body для if случится return - все блоки "одного уровня" возвращают результат

        res = None
        for element in node.childs:
            if self._rec_counter < self._rec_stack[-1]:
                break

            match element.t_type:
                # Парсим "верхний уровень" функции - доступны только определения функций, выражения типа '=' и вызовы
                case TokenType.OPERATOR:
                    res = self.__parse_expr(element) # Ищем присвоения на данном уровне
                case TokenType.KEYWORD:
                    match element.label:
                        case 'def':
                            self.__parse_def(element)
                        case 'if':
                            res = self.__parse_if(element)
                        case 'for':
                            res = self.__parse_for(element)
                        case 'while':
                            res = self.__parse_while(element)
                        case 'return':
                            # Особый случай - return составляет кортеж возврата и возвращает на уровень выше
                            res = self.__parse_list(element)
                            self._rec_counter -= 1
                            break
                        case _:
                            print(f"Unsuppoted body-level keyword: {element.label}")
                case TokenType.IDENTIFIER:
                    res = self.__parse_call_func(element)
                    # В данном случае только вызовы процедур

        return res # Возвращаем результат выполнения узла

    def __parse_def(self, node:TreeNode):
        '''
            Парсим определение функции
            На данном этапе нужно завести записть с идентификатором функции, для которой
            сопоставить таблицу аргументов и точку входа
        '''
        identifier = node.childs[0].label
        args_group = node.childs[1].childs

        meta_body = node.childs[2]
        local_frame = self._stack[-1]

        args_table = [] # Записи формата (Ident, Type[Type|Any], Default[None|Any])

        for arg in args_group:
            args_table.append([arg.label, None, None])
            for arg_desc in arg.childs: # Дескрипторы аргумента
                if arg_desc.t_type == TokenType.IDENTIFIER:
                    # Тип переменной
                    args_table[-1][1] = arg_desc.label
                elif arg_desc.t_type == TokenType.META:
                    # Значение по умолчанию
                    args_table[-1][2] = self.__parse_rval(arg_desc.childs[0])
        local_frame[identifier] = [args_table, meta_body]

    def __parse_if(self, node:TreeNode):
        self._stack.append(dict())
        self._rec_stack.append(self._rec_counter)


        condition = self.__parse_expr(node.childs[0])
        res = None
        if condition:
            res = self.__parse_node(node.childs[1])
        if len(node.childs) > 2:
            # Существует блок else
            res = self.__parse_node(node.childs[2])
        self._rec_stack.pop()
        self._stack.pop()
        return res

    def __parse_for(self, node:TreeNode):
        self._stack.append(dict())
        self._rec_stack.append(self._rec_counter)


        # Идентификатор для итераций
        ident = node.childs[0].label
        # Генераторы мы не могём - пока что делаем списки объектов
        objs = self.__parse_expr(node.childs[2])

        rec_level = self._rec_counter

        for i in objs:
            # Для каждого значения счётчика парсим тело
            self._stack[-1][ident] = i
            res = self.__parse_node(node.childs[3])

            if self._rec_counter < rec_level:
                self._stack.pop()
                self._rec_stack.pop()
                return res
        self._rec_stack.pop()
        self._stack.pop()
        return None

    def __parse_while(self, node:TreeNode):
        self._stack.append(dict())
        self._rec_stack.append(self._rec_counter)

        rec_level = self._rec_counter
        while self.__parse_expr(node.childs[0]):
            res = self.__parse_node(node.childs[1])
            if self._rec_counter < rec_level:
                self._rec_stack.pop()
                self._stack.pop()
                return res

        self._rec_stack.pop()
        self._stack.pop()
        return None

    def __parse_call_func(self, node: TreeNode):
        ''''''
        if node.childs[0].t_type != TokenType.META:
            # Если нашли составную функцию (через .)
            return self.__parse_call_func(node.childs[0])


        self._stack.append(dict())
        self._rec_counter += 1
        self._rec_stack.append(self._rec_counter)



        args = self.__parse_list(node.childs[0])

        res = None
        match node.label:
            case 'append':
                struct_lbl = node.parent.label
                struct, prnt_sg = self.__upscan_stack(struct_lbl)
                struct.append(args[0])
            case 'pop':
                struct_lbl = node.parent.label
                struct, prnt_sg = self.__upscan_stack(struct_lbl)
                struct.pop(*args)
            case 'extend':
                struct_lbl = node.parent.label
                struct, prnt_sg = self.__upscan_stack(struct_lbl)
                struct.extend(args)
            case 'print':
                print(*args)
            case 'input':
                res = input(*args)
            case 'range':
                res = range(*args)
            case _:
                signature, _ = self.__upscan_stack(node.label)
                arg_table = signature[0]
                for i in range(len(arg_table)):
                    # Устанавливаем пары паарметр - значение по умолчанию
                    self._stack[-1][arg_table[i][0]] = arg_table[i][2] 

                for i in range(min(len(args), len(arg_table))):
                    self._stack[-1][arg_table[i][0]] = args[i]

                res = self.__parse_node(signature[1])

        self._rec_counter -= 1
        self._rec_stack.pop()
        self._stack.pop()
        return res

    def __parse_expr(self, node:TreeNode):
        if node.t_type != TokenType.OPERATOR:
            # Если столкнулись с константой или результатом функции
            return self.__parse_rval(node)

        assign = False
        op = lambda x,y: y

        assign = node.label in ('+=', '-=', '=', '*=', '/=', '%=', '//=')
        pure_assign = node.label == '='

        arithm_part = node.label[:-1] if assign else node.label


        match arithm_part:
            case '+': op = lambda x,y: x + y
            case '-': op = lambda x,y: x - y
            case '*': op = lambda x,y: x * y
            case '/': op = lambda x,y: x / y
            case '%': op = lambda x,y: x % y
            case '//': op = lambda x,y: x // y
            case '<=': op = lambda x,y: x <= y
            case '<': op = lambda x,y: x < y
            case '>=': op = lambda x,y: x >= y
            case '>': op = lambda x,y: x > y
            case '==': op = lambda x,y: x == y
            case '!=': op = lambda x,y: x != y

        rv = self.__parse_rval(node.childs[1]) # Правое значение
        if assign:
            lv = self.__parse_lval(node.childs[0].childs[0])
            # Получаем кортеж из идентификатора и смещения (для массивов)
            if lv[1] is None: # Если получен просто идентификатор
                if not pure_assign:
                    lv_old, sg = self.__upscan_stack(lv[0])
                    res = op(lv_old, rv)
                    self._stack[sg][lv[0]] = res
                    return res
                else:
                    old, sg = self.__upscan_stack(lv[0])
                    if old is not None and self._rec_stack[sg] == self._rec_counter:
                        self._stack[sg][lv[0]] = rv
                    else:
                        self._stack[-1][lv[0]] = rv
                    return rv
            else: # Получена связка значение - индекс
                if not pure_assign:
                    lv_old, sg = self.__upscan_stack(lv[0])[lv[1]]
                    res = op(lv_old, rv)
                    self._stack[sg][lv[0]][lv[1]] = res
                    return res
                else:
                    old, sg = self.__upscan_stack(lv[0])
                    if old is not None and self._rec_stack[sg] == self._rec_counter:
                        self._stack[sg][lv[0]][lv[1]] = rv
                    else:
                        self._stack[-1][lv[0]][lv[1]] = rv
                    return rv
        else:
            lv = self.__parse_rval(node.childs[0])
            return op(lv, rv)
        

    def __parse_rval(self, node:TreeNode) -> any:
        '''
            исчисляемое выражение, возвращающее некоторое значение 
            В том числе отлавливает вложенные вызовы функций, массивы, операции
        '''
        match node.t_type:
            case TokenType.IDENTIFIER | TokenType.META:
                # Минимальный уровень вложенности
                # Варианты: а)переменная б)функция
                if node.t_subtype == Subtypes.MetaSubType.GROUP:
                    return self.__parse_list(node)
                
                if len(node.childs)>0 and node.childs[0].t_subtype == Subtypes.MetaSubType.FUNC_PARAMS:
                    return self.__parse_call_func(node)

                wnode = node
                if node.t_subtype == Subtypes.MetaSubType.LVAL:
                    wnode = node.childs[0]

                rv, sg = self.__upscan_stack(wnode.label)
                for ch in wnode.childs:
                    if ch.t_subtype == Subtypes.MetaSubType.INDEX:
                        idx = self.__parse_expr(ch.childs[0])
                        rv = rv[idx]
                return rv
            case TokenType.NUMBER_LITERAL:
                vf = float(node.label)
                v = int(node.label)
                if (v - vf) < 10**-12:
                    return v # Если целое
                else:
                    return vf # Если дробное
            case TokenType.STRING_LITERAL:
                return node.label
            case TokenType.OPERATOR:
                return self.__parse_expr(node)
            case _:
                raise ValueError(f'Unexpected rval: {node.t_type}, {node.label}')

    def __parse_lval(self, node:TreeNode) -> any:
        res = [node.label, None]
        for ch in node.childs:
            if ch.t_subtype == Subtypes.MetaSubType.INDEX:
                if res[1] is not None:
                    res[0] = res[0][res[1]]
                res[1] = self.__parse_expr(ch.childs[0])
        return res

    def __parse_list(self, node:TreeNode):
        res = []
        for element in node.childs:
            # Для каждого элемента списка
            res.append(self.__parse_rval(element))                
        return res

    def __upscan_stack(self, identificator):
        for i in range(len(self._stack)-1, -1, -1):
            val = self._stack[i].get(identificator, None)
            if val is not None:
                return (val, i)
        return (None, None)