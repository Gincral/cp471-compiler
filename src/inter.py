import re

class Quadruple:
    def __init__(self, op, arg1, arg2, result):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result
    
    def print():
        if arg2 is None and op is None:
            return f"{result} = {arg1}"
        elif arg2 is None:
            return f"{result} = {op} {arg1}"
        else:
            return f"{result} = {arg1} {op} {arg2}"

class ThreeAddressCode:
    def __init__(self):
        self.code = []
        self.labels = 0
        self.temps = 0
        self.expectingLabel = None

    def addCode(self, line):
        if self.expectingLabel is not None:
            self.code.append(f"{self.expectingLabel}: {line}")
            self.expectingLabel = None
        else:
            self.code.append(f"    {line}")

    def getCode(self):
        return self.code

    def printCode(self):
        print("Intermediate Code:")
        for line in self.code:
            print(line)

    def addLabel(self):
        self.labels += 1
        return f"L{self.labels}"
        
    def expectLabel(self):
        self.expectingLabel = f"L{self.labels}"

    def addTemp(self):
        self.temps += 1
        return f"t{self.temps}"

threeAddr = ThreeAddressCode()

def walkTree(tree):
    root = tree
    print("hi")
    if root.type == "stmt":
        print("we're at the stmt")
        walkStmt(root)
    threeAddr.printCode()

def walkStmt(root):
    print("What kind of statements are here?")
    for child in root.children:
        print(child.type)
    if root.children[0].type == "ifstmt":
        print("we're at the ifstmt")
        walkIfStmt(root.children[0])
        for child in root.children:
            print(child.type)
            if child.type == "stmt":
                print("ELSE DETECTED")
                label = threeAddr.addLabel()
                threeAddr.addCode(f"goto {label}")
                threeAddr.expectLabel()
                print("STMT DETECTED")
                walkStmt(child)
    else:
        root = root.children[0]
        if root.type == "dec":
            print("we're at the dec")
            walkDec(root)
        elif root.type == "assign":
            print("we're at the assign")
            walkAssign(root)
        elif root.type == "println":
            print("we're at the println")
            walkPrintln(root)

def walkPrintln(root):
    print("PRINTLN DETECTED")
    boolNode = None
    for child in root.children:
        if child.type == "bool":
            boolNode = child
    temp = walkBool(boolNode)
    threeAddr.addCode(f"call print, {temp}")

def walkDec(root):
    print(len(root.children))
    toAssign = root.children[2]
    root = root.children[-1]
    if root.type == "bool":
        print("we're at the bool")
        line = f"{toAssign.value.value} = {walkBool(root)}"
        threeAddr.addCode(line)
        print(line)

def walkAssign(root):
    toAssign = root.children[0]
    root = root.children[-1]
    if root.type == "bool":
        print("we're at the bool")
        line = f"{toAssign.value.value} = {walkBool(root)}"
        threeAddr.addCode(line)
        print(line)

def walkIfStmt(root):
    # if (1 < 2): { if(4 > 3): { print("1") } else:{ print("2") } } else: { print("3")}
    print("walking ifstmt")
    for child in root.children:
        print(child.type)
        if child.type == "bool":
            label = threeAddr.addLabel()
            line = f"if {walkBool(child)} goto {label}"
            threeAddr.addCode(line)
            threeAddr.expectLabel()
        elif child.type == "stmt":
            walkStmt(child)


def walkBool(root):
    if len(root.children) == 1:
        root = root.children[0]
        if root.type == "equality":
            print("we're at the equality")
            return walkEquality(root)
    else:
        line = f"{walkEquality(root.children[0])} {walkBool1(root.children[1])}"
        return line
    
def walkBool1(root):
# TODO
    print("im bool1")
    print(root.children[0].type)
    print(root.children[1].type)
    if root.children[1].type == "equality":
        print("we've got an equality")
        compare = root.children[0].value.value
        if len(root.children) > 2:
            print("haha")
            # TODO this works but isn't correct
            # line = f"{walkEquality(root.children[1])} {walkBool1(root.children[2])}"
            # return line
            line = f"{walkEquality(root.children[1])}"
            tokens = line.split(" ")
            print(tokens)
            temp = threeAddr.addTemp() 
            new_temp = temp
            if len(tokens) > 2:
                threeAddr.addCode(f"{temp} = {tokens[0]} {tokens[1]} {tokens[2]}")
                i = 3
                while i < len(tokens) - 1:
                    print(i)
                    new_temp = threeAddr.addTemp()
                    token_oper = tokens[i]
                    i += 1
                    token_value = tokens[i]
                    i += 1
                    threeAddr.addCode(f"{new_temp} = {temp} {token_oper} {token_value}")
                    temp = new_temp
            else:
                threeAddr.addCode(f"{temp} = {tokens[0]}")
            threeAddr.printCode()
            return f"{compare} {new_temp}"
        else:
            line = f"{walkEquality(root.children[1])} {walkBool1(root.children[2])}"
            return line


def walkEquality(root):
    if len(root.children) == 1:
        root = root.children[0]
        if root.type == "relation":
            print("we're at the relation")
            return walkRelation(root)
    else:
        line = f"{walkRelation(root.children[0])} {walkEquality1(root.children[1])}"
        return line

def walkEquality1(root):
    # TODO
    print(root.children[0].type)
    print(root.children[1].type)
    if len(root.children) == 2:
        print("let us go equality1")
        compare = root.children[0].value.value
        line = f"{compare} {walkRelation(root.children[1])}"
        print(line)
        # return line
        tokens = line.split(" ")
        print(tokens)
        temp = threeAddr.addTemp()
        new_temp = temp
        if len(tokens) > 2:
            print("creating temps for equality1")
            print(tokens)
            threeAddr.addCode(f"{temp} = {tokens[0]} {tokens[1]} {tokens[2]}")
            i = 3
            while i < len(tokens) - 1:
                print(i)
                new_temp = threeAddr.addTemp()
                token_oper = tokens[i]
                i += 1
                token_value = tokens[i]
                i += 1
                threeAddr.addCode(f"{new_temp} = {temp} {token_oper} {token_value}")
                temp = new_temp
        else:
            threeAddr.addCode(f"{temp} = {tokens[0]}")
    else:
        print("let us go equality1")
        compare = root.children[0].value.value
        line = f"{compare} {walkRelation(root.children[1])}"
        print(line)
        # return line
        tokens = line.split(" ")
        print(tokens)
        temp = threeAddr.addTemp()
        new_temp = temp
        if len(tokens) > 2:
            print("creating temps for equality1")
            print(tokens)
            threeAddr.addCode(f"{temp} = {tokens[0]} {tokens[1]} {tokens[2]}")
            i = 3
            while i < len(tokens) - 1:
                print(i)
                new_temp = threeAddr.addTemp()
                token_oper = tokens[i]
                i += 1
                token_value = tokens[i]
                i += 1
                threeAddr.addCode(f"{new_temp} = {temp} {token_oper} {token_value}")
                temp = new_temp
        threeAddr.printCode()
        return f"{oper} {new_temp}"

def walkRelation(root):
    if len(root.children) == 1:
        root = root.children[0]
        if root.type == "expr":
            print("we're at the expr")
            return walkExpr(root)
    else:
        line = f"{walkExpr(root.children[0])} {walkRelation1(root.children[1])}"
        return line

def walkRelation1(root):
    if len(root.children) == 2:
        print("rewrsdf")
        print(root.children[0].type)
        line = f"{walkCompar(root.children[0])} {walkExpr(root.children[1])}"
        return line
    else:
        line = f"{walkCompar(root.children[0])} {walkExpr(root.children[1])} {walkRelation1(root.children[2])}"
        return line
        print("haihdasd")

def walkCompar(root):
    print("whats the comparison?")
    print(root.value.value)
    return root.value.value

def walkExpr(root):
    print(root.type)
    print(len(root.children))
    if len(root.children) == 1:
        root = root.children[0]
        if root.type == "term":
            print("we're at the term")
            return walkTerm(root)
    else:
        if root.children[0].type == "term" and root.children[1].type == "expr'":
            print("we've got a term and an expr1")
            line = f"{walkTerm(root.children[0])} {walkExpr1(root.children[1])}"
            print(f"walkExpr received: {line}")
            temp = threeAddr.addTemp()
            threeAddr.addCode(f"{temp} = {line}")
            return temp
        print(line)
    
def walkExpr1(root):
    print("expr1:")
    print(len(root.children))
    # TODO handle recursive expr1
    if len(root.children) == 1:
        print('idk')
    else:
        print(root.children[0].type)
        print(root.children[1].type)
        if root.children[1].type == "term":
            print("we've got a term")
            oper = root.children[0].value.value
            line = f"{walkTerm(root.children[1])}"
            print(line)
            tokens = line.split(" ")
            print(tokens)
            temp = threeAddr.addTemp()
            new_temp = temp
            if len(tokens) > 2:
                threeAddr.addCode(f"{temp} = {tokens[0]} {tokens[1]} {tokens[2]}")
                i = 3
                while i < len(tokens) - 1:
                    print(i)
                    new_temp = threeAddr.addTemp()
                    token_oper = tokens[i]
                    i += 1
                    token_value = tokens[i]
                    i += 1
                    threeAddr.addCode(f"{new_temp} = {temp} {token_oper} {token_value}")
                    temp = new_temp
            else:
                threeAddr.addCode(f"{temp} = {tokens[0]}")
            return f"{oper} {new_temp}"

def walkTerm(root):
    print(len(root.children))
    if len(root.children) == 1:
        root = root.children[0]
        if root.type == "factor":
            print("we're at the factor")
            return walkFactor(root)
    else:
        if root.children[0].type == "factor" and root.children[1].type == "term'":
            print("we've got a factor and a term1")
            line = f"{walkFactor(root.children[0])} {walkTerm1(root.children[1])}"
            print(line)
            return line

def walkTerm1(root):
    if len(root.children) == 2:
        line = f"{root.children[0].value.value} {walkFactor(root.children[1])}"
    else:
        line = f"{root.children[0].value.value} {walkFactor(root.children[1])} {walkTerm1(root.children[2])}"
    return line


def walkFactor(root):
    print("whats the value?")
    print(root.value[0].value)
    return root.value[0].value

def inter(symbolTable, tree):
    inter = []
    print(tree.value[0].value)
    walkTree(tree)
    three_address_split = []
    for line in threeAddr.getCode():
        three_address_split.append(line.split(" "))
    # printIntermediate(three_address)
    # print("===============")


def getThreeAddr():
    return threeAddr.getCode()