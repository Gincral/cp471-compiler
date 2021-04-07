from symbol import Data

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

def parser (symbolTable, tokenList):
    if (tokenList[len(tokenList)-1].value == ';'): tokenList = tokenList[:len(tokenList)-1]
    stmtN = Node(tokenList)
    stmt(stmtN)

    return None

def stmt(root):
    print("Grammar stmt")
    tokenList = root.value
    if tokenList[0].type == 'id':
        assignN = Node(tokenList)
        root.children.append(assignN)
        return assign(assignN)
    else:
        if tokenList[0].value == 'if':
            le = len(tokenList)
            count = 0
            for i in range(le):
                if tokenList[i].value == '{':
                    count += 1
                elif tokenList[i].value == '}':
                    count -= 1
                    if count == 0 and i < le-4 and tokenList[i+1].value == 'else':
                        if tokenList[i+2].value == ':' and tokenList[i+3].value == '{' and tokenList[le-1].value == '}':
                            print("Grammar ifstmt else")
                            ifstmtN = Node(tokenList[:i+1])
                            root.children.append(ifstmtN)
                            root.children.append(Node(tokenList[i+1]))
                            root.children.append(Node(tokenList[i+2]))
                            root.children.append(Node(tokenList[i+3]))
                            stmtN = Node(tokenList[i+4:le-1])
                            root.children.append(stmtN)
                            root.children.append(Node(tokenList[le-1]))
                            return ifstmt(ifstmtN) and stmt(stmtN)
                        else:
                            print("wrong grammar: stmt")
                            return False
            print(count)
            if count == 0:
                ifstmtN = Node(tokenList)
                root.children.append(ifstmtN)
                return ifstmt(ifstmtN)
            else:
                print("wrong grammar: stmt, bracket number invalid")
                return False
        elif tokenList[0].value == 'print':
            printN = Node(tokenList)
            root.children.append(printN)
            return println(printN)
        elif tokenList[0].value == 'def':
            decN = Node(tokenList)
            root.children.append(decN)
            return dec(decN)
        else:
            print("wrong grammar: stmt")
            return False
        
def ifstmt(root):
    print("Grammar ifstmt")
    tokenList = root.value
    le = len(tokenList)
    for i in range(le):
        if tokenList[i].value == ')': 
            break
    if i < le-3 and tokenList[1].value == '(' and tokenList[i].value ==')' and tokenList[i+1].value ==':' and tokenList[i+2].value =='{' and tokenList[le-1].value =='}': 
        root.children.append(Node(tokenList[0]))
        root.children.append(Node(tokenList[1]))
        boolN = Node(tokenList[2:i])
        root.children.append(boolN)
        root.children.append(Node(tokenList[i]))
        root.children.append(Node(tokenList[i+1]))
        root.children.append(Node(tokenList[i+2]))
        stmtN = Node(tokenList[i+3:le-1])
        root.children.append(stmtN)
        root.children.append(Node(tokenList[le-1]))
        return bool(boolN) and stmt(stmtN)
    else:
        print("wrong grammar: ifstmt")
        return False
    
def println(root):
    print("Grammar println")
    tokenList = root.value
    le = len(tokenList)
    if tokenList[1].value == '(' and tokenList[le-1].value == ')':
        boolN = Node(tokenList[2:le-1])
        root.children.append(Node(tokenList[0]))
        root.children.append(Node(tokenList[1]))
        root.children.append(boolN)
        root.children.append(Node(tokenList[le-2]))
        root.children.append(Node(tokenList[le-1]))
        return bool(boolN)
    else:
        print("wrong grammar: println")
        return False

def dec(root):
    print("Grammar dec")
    tokenList = root.value
    le = len(tokenList)
    if tokenList[1].type == 'lex' and tokenList[2].type == 'id' and tokenList[3].value == '=':
        boolN = Node(tokenList[2:le-2])
        root.children.append(Node(tokenList[0]))
        root.children.append(Node(tokenList[1]))
        root.children.append(boolN)
        root.children.append(Node(tokenList[le-2]))
        root.children.append(Node(tokenList[le-1]))
        return bool(boolN)
    else:
        print("wrong grammar: println")
        return False

def assign(root):
    print("Grammar assign")
    tokenList = root.value
    if tokenList[1].value == '=':
        boolN = Node(tokenList[2:])
        root.children.append(Node(tokenList[0]))
        root.children.append(Node(tokenList[1]))
        root.children.append(boolN)
        return bool(boolN)
    else:
        print("wrong grammar: assign")
        return False

def bool(root):
    print("Grammar bool")
    tokenList = root.value
    for i in range(len(tokenList)):
        if tokenList[i].value == '||' or tokenList[i].value == '&&':
            equalityN = Node(tokenList[:i])
            bool1N =  Node(tokenList[i:])
            root.children.append(Node(equalityN))
            root.children.append(Node(bool1N))
            return equality(equalityN) and bool1(bool1N)
    equalityN = Node(tokenList)
    root.children.append(Node(equalityN))
    return equality(equalityN)

def bool1(root):
    print("Grammar bool1")
    tokenList = root.value
    root.children.append(Node(tokenList[0]))
    tokenList = tokenList[1:]
    for i in range(len(tokenList)):
        if tokenList[i].value == '||' or tokenList[i].value == '&&':
            equalityN = Node(tokenList[:i])
            bool1N =  Node(tokenList[i:])
            root.children.append(Node(equalityN))
            root.children.append(Node(bool1N))
            return equality(equalityN) and bool1(bool1N)
    equalityN = Node(tokenList)
    root.children.append(Node(equalityN))
    return equality(equalityN)

def equality(root):
    print("Grammar equality")
    tokenList = root.value
    for i in range(len(tokenList)):
        if tokenList[i].value == '==' or tokenList[i].value == '!=':
            relationN = Node(tokenList[:i])
            equalityN =  Node(tokenList[i:])
            root.children.append(Node(relationN))
            root.children.append(Node(equalityN))
            return relation(relationN) and equality1(equalityN)
    relationN = Node(tokenList)
    root.children.append(Node(relationN))
    return relation(relationN)

def equality1(root):
    print("Grammar equality1")
    tokenList = root.value
    root.children.append(Node(tokenList[0]))
    tokenList = tokenList[1:]
    for i in range(len(tokenList)):
        if tokenList[i].value == '==' or tokenList[i].value == '!=':
            relationN = Node(tokenList[:i])
            equalityN =  Node(tokenList[i:])
            root.children.append(Node(relationN))
            root.children.append(Node(equalityN))
            return relation(relationN) and equality1(equalityN)
    relationN = Node(tokenList)
    root.children.append(Node(relationN))
    return relation(relationN)

def relation(root):
    print("Grammar relation")
    tokenList = root.value
    for i in range(len(tokenList)):
        if tokenList[i].value == '<' or tokenList[i].value == '>' or tokenList[i].value == '>=' or tokenList[i].value == '<=':
            exprN = Node(tokenList[:i])
            relationN =  Node(tokenList[i:])
            root.children.append(Node(exprN))
            root.children.append(Node(relationN))
            return expr(exprN) and relation1(relationN)
    exprN = Node(tokenList)
    root.children.append(Node(exprN))
    return expr(exprN)

def relation1(root):
    print("Grammar relation1")
    tokenList = root.value
    root.children.append(Node(tokenList[0]))
    tokenList = tokenList[1:]
    for i in range(len(tokenList)):
        if tokenList[i].value in ['<', '>', '<=', '>=']:
            exprN = Node(tokenList[:i])
            relationN =  Node(tokenList[i:])
            root.children.append(Node(exprN))
            root.children.append(Node(relationN))
            return expr(exprN) and relation1(relationN)
    exprN = Node(tokenList)
    root.children.append(Node(exprN))
    return expr(exprN)

def expr(root):
    print("Grammar expr")
    tokenList = root.value
    for i in range(len(tokenList)):
        if tokenList[i].value == '+' or tokenList[i].value == '-':
            termN = Node(tokenList[:i])
            exprN =  Node(tokenList[i:])
            root.children.append(Node(termN))
            root.children.append(Node(exprN))
            return term(termN) and expr1(exprN)
    termN = Node(tokenList)
    root.children.append(Node(termN))
    return term(termN)

def expr1(root):
    print("Grammar expr1")
    tokenList = root.value
    root.children.append(Node(tokenList[0]))
    tokenList = tokenList[1:]
    for i in range(len(tokenList)):
        if tokenList[i].value == '+' or tokenList[i].value == '-':
            termN = Node(tokenList[:i])
            exprN =  Node(tokenList[i:])
            root.children.append(Node(termN))
            root.children.append(Node(exprN))
            return term(termN) and expr1(exprN)
    termN = Node(tokenList)
    root.children.append(Node(termN))
    return term(termN)

def term(root):
    print("Grammar term")
    tokenList = root.value
    for i in range(len(tokenList)):
        if tokenList[i].value in ['*', '/', '%', '//']:
            factorN = Node(tokenList[:i])
            termN =  Node(tokenList[i:])
            root.children.append(Node(factorN))
            root.children.append(Node(termN))
            return factor(factorN) and term1(termN)
    factorN = Node(tokenList)
    root.children.append(Node(factorN))
    return factor(factorN)

def term1(root):
    print("Grammar term1")
    tokenList = root.value
    root.children.append(Node(tokenList[0]))
    tokenList = tokenList[1:]
    for i in range(len(tokenList)):
        if tokenList[i].value in ['*', '/', '%', '//']:
            factorN = Node(tokenList[:i])
            termN =  Node(tokenList[i:])
            root.children.append(Node(factorN))
            root.children.append(Node(termN))
            return factor(factorN) and term1(termN)
    factorN = Node(tokenList)
    root.children.append(Node(factorN))
    return factor(factorN)

def factor(root):
    print("Grammar factor")
    tokenList = root.value #len of token list should be 1
    print(tokenList[0].value)
    if len(tokenList) == 1: 
        root.children.append(Node(tokenList[0]))
        return True
    else:
        print("len of token list should be 1")
        return False
