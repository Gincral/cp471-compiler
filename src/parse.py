from symbol import Data


class Node:
    def __init__(self, value, type=None):
        self.value = value
        self.type = type
        self.children = []

def parse(symbolTable, tokenList):
    global SymbolTable
    SymbolTable = symbolTable

    # Delete end of line symbol e.g. ";"
    # In some condition the position of ";" is not at the end, e.g. if(boolean): {print("a");} 
    index = 0
    while index < len(tokenList):
        if (tokenList[index].value == ";"):
            tokenList.pop(index)
        else:
            index+=1

    stmtN = Node(tokenList, "stmt")
    if (stmt(stmtN)):
        return stmtN
    

def stmt(root):
    print("Grammar stmt")
    tokenList = root.value
    if tokenList[0].type == 'id':
        assignN = Node(tokenList, "assign")
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
                            ifstmtN = Node(tokenList[:i+1], "ifstmt")
                            root.children.append(ifstmtN)
                            root.children.append(Node(tokenList[i+1]))
                            root.children.append(Node(tokenList[i+2]))
                            root.children.append(Node(tokenList[i+3]))
                            stmtN = Node(tokenList[i+4:le-1], "stmt")
                            root.children.append(stmtN)
                            root.children.append(Node(tokenList[le-1]))
                            return ifstmt(ifstmtN) and stmt(stmtN)
                        else:
                            print("wrong grammar: stmt")
                            return False
            print(count)
            if count == 0:
                ifstmtN = Node(tokenList, "ifstmt")
                root.children.append(ifstmtN)
                return ifstmt(ifstmtN)
            else:
                print("wrong grammar: stmt, bracket number invalid")
                return False
        elif tokenList[0].value == 'print':
            printN = Node(tokenList, "println")
            root.children.append(printN)
            return println(printN)
        elif tokenList[0].value == 'def':
            decN = Node(tokenList, "dec")
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
        boolN = Node(tokenList[2:i], "bool")
        root.children.append(boolN)
        root.children.append(Node(tokenList[i]))
        root.children.append(Node(tokenList[i+1]))
        root.children.append(Node(tokenList[i+2]))
        stmtN = Node(tokenList[i+3:le-1], "stmt")
        root.children.append(stmtN)
        root.children.append(Node(tokenList[le-1]))
        if bool(boolN) == 'boolean': return stmt(stmtN)
        else: 
            print("ifstmt error, condition should be boolean")
            return False
    else:
        print("wrong grammar: ifstmt")
        return False
    
def println(root):
    print("Grammar println")
    tokenList = root.value
    le = len(tokenList)
    if tokenList[1].value == '(' and tokenList[le-1].value == ')':
        boolN = Node(tokenList[2:le-1], "bool")
        root.children.append(Node(tokenList[0]))
        root.children.append(Node(tokenList[1]))
        root.children.append(boolN)
        root.children.append(Node(tokenList[le-1]))
        return bool(boolN)
    else:
        print("wrong grammar: println")
        return False

def dec(root):
    print("Grammar dec")
    tokenList = root.value
    le = len(tokenList)
    if tokenList[1].type == 'lex' and tokenList[1].value in ['string', 'boolean', 'number'] and tokenList[2].type == 'id' and tokenList[3].value == '=':
        data = Data(tokenList[2].value, tokenList[1].value, None)
        SymbolTable.appendData(data)
        root.children.append(Node(tokenList[0], "def"))
        root.children.append(Node(tokenList[1], "type"))
        root.children.append(Node(tokenList[2], "id"))
        root.children.append(Node(tokenList[3], "="))
        boolN = Node(tokenList[4:], "bool")
        root.children.append(boolN)
        if bool(boolN) == tokenList[1].value : 
            return True
        else:
            print("Dec Error: declare type wrong")
    else:
        print("wrong grammar: dec")
        return False

def assign(root): 
    print("Grammar assign")
    tokenList = root.value
    if tokenList[1].value == '=':
        boolN = Node(tokenList[2:], "bool")
        root.children.append(Node(tokenList[0], "id"))
        root.children.append(Node(tokenList[1], "="))
        root.children.append(boolN)
        data = SymbolTable.searchData(tokenList[0].value)
        if data and data.type == bool(boolN): return True
        elif not data:
            print('Assign error: variable didnt get assign')
            return False
        else: 
            print('Assign error: assign value is not the right type')
            return False
    else:
        print("wrong grammar: assign")
        return False

def bool(root):
    print("Grammar bool")
    tokenList = root.value
    for i in range(len(tokenList)):
        if tokenList[i].value == '||' or tokenList[i].value == '&&' or tokenList[i].value == "and" or tokenList[i].value == "or":
            equalityN = Node(tokenList[:i], "equality")
            bool1N =  Node(tokenList[i:], "bool'")
            root.children.append(equalityN)
            root.children.append(bool1N)
            type = equality(equalityN)
            if type == bool1(bool1N) and type != False:
                return 'boolean'
            else: 
                print("Bool error, two variables have different type")
                return False 
    equalityN = Node(tokenList, "equality")
    root.children.append(equalityN)
    return equality(equalityN) 

def bool1(root):
    print("Grammar bool1")
    tokenList = root.value
    root.children.append(Node(tokenList[0], tokenList[0].value))
    tokenList = tokenList[1:]
    for i in range(len(tokenList)):
        if tokenList[i].value == '||' or tokenList[i].value == '&&' or tokenList[i].value == "and" or tokenList[i].value == "or":
            equalityN = Node(tokenList[:i], "equality")
            bool1N =  Node(tokenList[i:], "bool1")
            root.children.append(equalityN)
            root.children.append(bool1N)
            type = equality(equalityN)
            if type == bool1(bool1N) and type != False:
                return 'boolean'
            else: 
                print("Bool1 error, two variables have different type")
                return False 
    equalityN = Node(tokenList, "equality")
    root.children.append(equalityN)
    return equality(equalityN)

def equality(root):
    print("Grammar equality")
    tokenList = root.value
    for i in range(len(tokenList)):
        if tokenList[i].value == '==' or tokenList[i].value == '!=':
            relationN = Node(tokenList[:i], "relation")
            equalityN =  Node(tokenList[i:], "equality'")
            root.children.append(relationN)
            root.children.append(equalityN)
            type = relation(relationN)
            if type == equality1(equalityN) and type != False:
                return 'boolean'
            else: 
                print("Equality error, two variables have different type")
                return False 
    relationN = Node(tokenList, "relation")
    root.children.append(relationN)
    return relation(relationN)

def equality1(root):
    print("Grammar equality1")
    tokenList = root.value
    root.children.append(Node(tokenList[0], tokenList[0].value))
    tokenList = tokenList[1:]
    for i in range(len(tokenList)):
        if tokenList[i].value == '==' or tokenList[i].value == '!=':
            relationN = Node(tokenList[:i], "relation")
            equalityN =  Node(tokenList[i:], "equality1")
            root.children.append(relationN)
            root.children.append(equalityN)
            type = relation(relationN)
            if type == equality1(equalityN) and type != False:
                return 'boolean'
            else: 
                print("Equality1 error, two variables have different type")
                return False 
    relationN = Node(tokenList, "relation")
    root.children.append(relationN)
    return relation(relationN)

def relation(root):
    print("Grammar relation")
    tokenList = root.value
    for i in range(len(tokenList)):
        if tokenList[i].value == '<' or tokenList[i].value == '>' or tokenList[i].value == '>=' or tokenList[i].value == '<=':
            exprN = Node(tokenList[:i], "expr")
            relationN =  Node(tokenList[i:], "relation'")
            root.children.append(exprN)
            root.children.append(relationN)
            type = expr(exprN)
            if type == relation1(relationN) and type != False:
                return 'boolean'
            else: 
                print("Relation error, two variables have different type")
                return False 
    exprN = Node(tokenList, "expr")
    root.children.append(exprN)
    return expr(exprN)

def relation1(root):
    print("Grammar relation1")
    tokenList = root.value
    root.children.append(Node(tokenList[0], tokenList[0].value))
    tokenList = tokenList[1:]
    for i in range(len(tokenList)):
        if tokenList[i].value in ['<', '>', '<=', '>=']:
            exprN = Node(tokenList[:i], "expr")
            relationN =  Node(tokenList[i:], "relation'")
            root.children.append(exprN)
            root.children.append(relationN)
            type = expr(exprN)
            if type == relation1(relationN) and type != False:
                return 'boolean'
            else: 
                print("Relation1 error, two variables have different type")
                return False 
    exprN = Node(tokenList, "expr")
    root.children.append(exprN)
    return expr(exprN)

def expr(root):
    print("Grammar expr")
    tokenList = root.value
    for i in range(len(tokenList)):
        if tokenList[i].value == '+' or tokenList[i].value == '-':
            termN = Node(tokenList[:i], "term")
            exprN =  Node(tokenList[i:], "expr'")
            root.children.append(termN)
            root.children.append(exprN)
            type = term(termN)
            if type == expr1(exprN) and type != False:
                return type
            else: 
                print("Expr error, two variables have different type")
                return False 
    termN = Node(tokenList, "term")
    root.children.append(termN)
    return term(termN)

def expr1(root):
    print("Grammar expr1")
    tokenList = root.value
    root.children.append(Node(tokenList[0], tokenList[0].value))
    tokenList = tokenList[1:]
    for i in range(len(tokenList)):
        if tokenList[i].value == '+' or tokenList[i].value == '-':
            termN = Node(tokenList[:i], "term")
            exprN =  Node(tokenList[i:], "expr'")
            root.children.append(termN)
            root.children.append(exprN)
            type = term(termN)
            if type == expr1(exprN) and type != False:
                return type
            else: 
                print("Expr1 error, two variables have different type")
                return False 
    termN = Node(tokenList, "term")
    root.children.append(termN)
    return term(termN)

def term(root):
    print("Grammar term")
    tokenList = root.value
    for i in range(len(tokenList)):
        if tokenList[i].value in ['*', '/', '%', '//']:
            factorN = Node(tokenList[:i], "factor")
            termN =  Node(tokenList[i:], "term'")
            root.children.append(factorN)
            root.children.append(termN)
            type = factor(factorN)
            if type == term1(termN) and type != False:
                return type
            else: 
                print("Term error, two variables have different type")
                return False 
    factorN = Node(tokenList, "factor")
    root.children.append(factorN)
    return factor(factorN)

def term1(root):
    print("Grammar term1")
    tokenList = root.value
    root.children.append(Node(tokenList[0]))
    tokenList = tokenList[1:]
    for i in range(len(tokenList)):
        if tokenList[i].value in ['*', '/', '%', '//']:
            factorN = Node(tokenList[:i], "factor")
            termN =  Node(tokenList[i:], "term'")
            root.children.append(factorN)
            root.children.append(termN)
            type = factor(factorN)
            if type == term1(termN) and type != False:
                return type
            else: 
                print("Term1 error, two variables have different type")
                return False 
    factorN = Node(tokenList, "factor")
    root.children.append(factorN)
    return factor(factorN)

def factor(root):
    print("Grammar factor")
    tokenList = root.value #len of token list should be 1
    print(tokenList[0].value, tokenList[0].type)
    if len(tokenList) == 1 or (len(tokenList) == 2 and tokenList[1].value == ";"): 
        root.children.append(Node(tokenList[0], "value"))
        if tokenList[0].type == "id":
            data = SymbolTable.searchData(tokenList[0].value)
            return data.type
        return tokenList[0].type
    else:
        print("len of token list should be 1")
        return False
