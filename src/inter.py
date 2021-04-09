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
        self.expectingLabel = []

    def addCode(self, line):
        if len(self.expectingLabel) > 0 and not line.startswith("goto"):
            label = ""
            # if line.startswith("if"):
            #     label = self.expectingLabel.pop(0)
            # else:
            #     label = self.expectingLabel.pop()
            label = self.expectingLabel.pop(0)
            self.code.append(f"{label}: {line}")
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
        
    def expectLabel(self, label):
        self.expectingLabel.append(label)

    def addTemp(self):
        self.temps += 1
        return f"t{self.temps}"

threeAddr = ThreeAddressCode()

def walkTree(tree):
    root = tree
    print("hi")
    if root.type == "stmt":
        print("walking stmt")
        walkStmt(root)
    threeAddr.printCode()

def walkStmt(root):
    # print("What kind of statements are here?")
    # for child in root.children:
    #     print(child.type)
    if root.children[0].type == "ifstmt":
        print("walking ifstmt")
        walkIfStmt(root.children[0])
        for child in root.children:
            if child.type == "stmt":
                print("ELSE DETECTED")
                # label = threeAddr.addLabel()
                # threeAddr.addCode(f"goto {label}")
                # threeAddr.expectLabel(label)
                walkStmt(child)
    else:
        root = root.children[0]
        if root.type == "dec":
            print("walking dec")
            walkDec(root)
        elif root.type == "assign":
            print("walking assign")
            walkAssign(root)
        elif root.type == "println":
            print("walking println")
            walkPrintln(root)

def walkPrintln(root):
    boolNode = None
    for child in root.children:
        if child.type == "bool":
            boolNode = child
    temp = walkBool(boolNode)
    threeAddr.addCode(f"call print, {temp}")

def walkDec(root):
    toAssign = root.children[2]
    root = root.children[-1]
    if root.type == "bool":
        print("walking bool")
        line = f"{toAssign.value.value} = {walkBool(root)}"
        threeAddr.addCode(line)

def walkAssign(root):
    toAssign = root.children[0]
    root = root.children[-1]
    if root.type == "bool":
        print("walking bool")
        line = f"{toAssign.value.value} = {walkBool(root)}"
        threeAddr.addCode(line)

def walkIfStmt(root):
    # if (1 < 2): { if(4 > 3): { print("1") } else:{ print("2") } } else: { print("3")}
    print("walking ifstmt")
    for child in root.children:
        if child.type == "bool":
            label1 = threeAddr.addLabel()
            line = f"if {walkBool(child)} goto {label1}"
            threeAddr.addCode(line)
            label2 = threeAddr.addLabel()
            line = f"goto {label2}"
            threeAddr.addCode(line)
            threeAddr.expectLabel(label1)
            threeAddr.expectLabel(label2)
        elif child.type == "stmt":
            walkStmt(child)


def walkBool(root):
    if len(root.children) == 1:
        root = root.children[0]
        if root.type == "equality":
            print("walking equality")
            return walkEquality(root)
    else:
        line = f"{walkEquality(root.children[0])} {walkBool1(root.children[1])}"
        return line
    
def walkBool1(root):
# TODO
    print("walking bool1")
    if root.children[1].type == "equality":
        compare = root.children[0].value.value
        if len(root.children) > 2:
            print("mess")
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
            print("walking relation")
            return walkRelation(root)
    else:
        line = f"{walkRelation(root.children[0])} {walkEquality1(root.children[1])}"
        return line

def walkEquality1(root):
    print("walking equality1")
    if len(root.children) == 2:
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
            # print(tokens)
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
            # print(tokens)
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
            print("walking expr")
            return walkExpr(root)
    else:
        line = f"{walkExpr(root.children[0])} {walkRelation1(root.children[1])}"
        return line

def walkRelation1(root):
    if len(root.children) == 2:
        print(root.children[0].type)
        line = f"{walkCompar(root.children[0])} {walkExpr(root.children[1])}"
        return line
    else:
        line = f"{walkCompar(root.children[0])} {walkExpr(root.children[1])} {walkRelation1(root.children[2])}"
        return line

def walkCompar(root):
    print("whats the comparison?")
    print(root.value.value)
    return root.value.value

def walkExpr(root):
    if len(root.children) == 1:
        root = root.children[0]
        if root.type == "term":
            print("walking term")
            return walkTerm(root)
    else:
        if root.children[0].type == "term" and root.children[1].type == "expr'":
            print("running walkTerm and walkExpr1")
            line = f"{walkTerm(root.children[0])} {walkExpr1(root.children[1])}"
            print(f"walkExpr received: {line}")
            temp = threeAddr.addTemp()
            threeAddr.addCode(f"{temp} = {line}")
            return temp
        print(line)
    
def walkExpr1(root, useTemp=None, hasTerm=None):
    print("expr1:")
    # print(root.children[0].type)
    # print(root.children[1].type)
    if root.children[1].type == "term":
        print("running walkTerm")
        oper = root.children[0].type
        print(f"whats oper? {oper}")
        line = f"{walkTerm(root.children[1])}"
        # print(line)
        tokens = line.split(" ")
        # print(tokens)
        temp = threeAddr.addTemp()
        new_temp = temp
        print("what's the line that got returned?")
        print(line)
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
                print(f"ADDING: {new_temp} = {temp} {token_oper} {token_value}")
                threeAddr.addCode(f"{new_temp} = {temp} {token_oper} {token_value}")
                temp = new_temp
        # TODO do i need??
        elif len(tokens) > 1:
            print("im lost")
            print(tokens[0])
            print(tokens[1])
            threeAddr.addCode(f"{new_temp} = {useTemp} {tokens[0]} {tokens[1]}")
        else:
            if useTemp:
                threeAddr.addCode(f"{new_temp} = {useTemp} {oper} {tokens[0]}")
                return f"{new_temp}"
            else:
                print("yikes")
                # threeAddr.addCode(f"{new_temp} = {tokens[0]}")
        if len(root.children) > 2:
            line = walkExpr1(root.children[2], temp)
            tokens = line.split(" ")
            if len(tokens) == 1:
                new_temp = tokens[0]
            print("WHAT DID THIS RETURN?")
            print(new_temp)
            # return test
        # if len(root.)
        return f"{oper} {new_temp}"

def walkTerm(root):
    if len(root.children) == 1:
        root = root.children[0]
        if root.type == "factor":
            print("walking factor")
            return walkFactor(root)
    else:
        if root.children[0].type == "factor" and root.children[1].type == "term'":
            print("running walkFactor and walkTerm1")
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
    print("whats the factor?")
    return root.value[0].value

def inter(symbolTable, tree):
    inter = []
    walkTree(tree)
    three_address_split = []
    for line in threeAddr.getCode():
        three_address_split.append(line.split(" "))
    # printIntermediate(three_address)
    # print("===============")


def getThreeAddr():
    return threeAddr.getCode()