from symbol import Data

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

def parser (symbolTable, tokenList):
    if (tokenList[len(tokenList)-1].value == ';'): tokenList = tokenList[:len(tokenList)-1]
    root = Node(tokenList)
    stmt(root)
    return None

def stmt(root):
    print("Grammar stmt")
    tokenList = root.value
    if tokenList[0].type == 'id':
        node = Node(tokenList)
        root.children.append(node)
        return assign(node)
    else:
        if tokenList[0].value == 'if':
            return "haha"
        elif tokenList[0].value == 'print':
            node = Node(tokenList)
            root.children.append(node)
            return println(node)
        elif tokenList[0].value == 'def':
            node = Node(tokenList)
            root.children.append(node)
            return dec(node)
        else:
            print("wrong grammar: stmt")
            return ValueError
        

def ifstmt(root):
    print("Grammar ifstmt")
    return None

def println(root):
    print("Grammar println")
    tokenList = root.value
    le = len(tokenList)
    if tokenList[1].value == '(' and tokenList[le-1].value == ')':
        node = Node(tokenList[2:le-2])
        root.children.append(Node(tokenList[0]))
        root.children.append(Node(tokenList[1]))
        root.children.append(node)
        root.children.append(Node(tokenList[le-2]))
        root.children.append(Node(tokenList[le-1]))
        return bool(node)
    else:
        print("wrong grammar: println")
        return ValueError

def dec(root):
    print("Grammar dec")
    tokenList = root.value
    le = len(tokenList)
    if tokenList[1].type == 'lex' and tokenList[2].type == 'id' and tokenList[3].value == '=':
        node = Node(tokenList[2:le-2])
        root.children.append(Node(tokenList[0]))
        root.children.append(Node(tokenList[1]))
        root.children.append(node)
        root.children.append(Node(tokenList[le-2]))
        root.children.append(Node(tokenList[le-1]))
        return bool(node)
    else:
        print("wrong grammar: println")
        return ValueError

def assign(root):
    print("Grammar assign")
    tokenList = root.value
    if tokenList[1].value == '=':
        node = Node(tokenList[2:])
        root.children.append(Node(tokenList[0]))
        root.children.append(Node(tokenList[1]))
        root.children.append(node)
        return bool(node)
    else:
        print("wrong grammar: assign")
        return ValueError

def bool(root):
    print("Grammar bool")
    return None

def bool1(root):
    print("Grammar bool1")
    return None

def equality(root):
    print("Grammar equality")
    return None

def equality1(root):
    print("Grammar equality1")
    return None

def expr(root):
    print("Grammar expr")
    return None

def expr1(root):
    print("Grammar expr1")
    return None

def term(root):
    print("Grammar term")
    return None

def term1(root):
    print("Grammar term1")
    return None

def oper(root):
    print("Grammar term1")
    return None

def factor(root):
    print("Grammar term1")
    return None

def boolean(root):
    print("Grammar term1")
    return None