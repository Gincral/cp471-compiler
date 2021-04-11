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
        self.toBackPatch = []
        self.isCondition = []

    def addCode(self, line):
        print("TEST")
        print(f"we expect these labels: {self.expectingLabel}")
        print(f"we received this line: {line}")
        if len(self.expectingLabel) > 0 and not line.startswith("goto"):
            label = ""
            # if line.startswith("if"):
            #     label = self.expectingLabel.pop(0)
            # else:
            #     label = self.expectingLabel.pop()
            label = self.expectingLabel.pop(0)
            self.code.append(f"{label}: {line}")
            # Handle backpatch for OR condition
            if len(self.toBackPatch) > 0 and line.startswith("if"):
                if len(self.isCondition) > 0 and self.isCondition[0] == "||":
                    print("BACKPATCHING")
                    index = self.toBackPatch.pop(0)
                    self.isCondition.pop(0)
                    print(f"stored line = {self.code[index]}")
                    self.code[index] = self.code[index].replace("_", self.getLastLabel())
        elif len(self.toBackPatch) > 0 and line.startswith("goto"):
            self.code.append(f"    {line}")
            if len(self.isCondition) > 0 and self.isCondition[0] == "&&":
                index = self.toBackPatch.pop(0)
                self.isCondition.pop(0)
                print(f"stored line = {self.code[index]}")
                self.code[index] = self.code[index].replace("_", self.getLastLabel())
        else:
            self.code.append(f"    {line}")
            # if line.endswith("_"):
            #     print(f"ADDING TO BACKPATCH: {line}")
            #     self.toBackPatch.append(len(self.code) - 1)

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

    def expectBackPatch(self, condition):
        index = len(self.code) - 1
        if self.code[index].endswith("_"):
            print("ADDING TO BACKPATCH")
            self.toBackPatch.append(len(self.code) - 1)
            self.isCondition.append(condition)
        else:
            raise Exception("invalid backpatch request")

    def addTemp(self):
        self.temps += 1
        return f"t{self.temps}"

    def getLastTemp(self):
        return f"t{self.temps}"

    def getLastLabel(self):
        return f"L{self.labels}"

    # If all code has been generated but a label is still expected, remove the extraneous matching goto statement
    def cleanUpLabels(self):
        if len(self.expectingLabel) > 0:
            for i in range(len(self.expectingLabel)):
                label = self.expectingLabel.pop()
                for i in range(len(self.code) - 1):
                    if self.code[i].strip().startswith("goto") and self.code[i].endswith(label):
                        self.code.pop(i)
                        

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
        returnValue = walkBool(root)
        print(f"returnValue = {returnValue}")
        # TODO where is empty string coming from
        if returnValue is None or returnValue is "":
            line = f"{toAssign.value.value} = {threeAddr.getLastTemp()}"
            threeAddr.addCode(line)
        else:
            line = f"{toAssign.value.value} = {returnValue}"
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
            result = walkBool(child, fromIf=True)
            print(f"walkIfStmt received {result}")
            # If this is false assume the if stmt was already handled
            if result is not None and result is not "":
                label1 = threeAddr.addLabel()
                line = f"if {result} goto {label1}"
                threeAddr.addCode(line)
                label2 = threeAddr.addLabel()
                line = f"goto {label2}"
                threeAddr.addCode(line)
                threeAddr.expectLabel(label1)
                threeAddr.expectLabel(label2)
        elif child.type == "stmt":
            walkStmt(child)


def walkBool(root, fromIf=False):
    if len(root.children) == 1:
        root = root.children[0]
        if root.type == "equality":
            print("walking equality")
            result = walkEquality(root, fromIf=fromIf)
            print(f"walkbool returning: {result}")
            return result
    else:
        equality = walkEquality(root.children[0], fromIf=fromIf)
        line = walkBool1(root.children[1], hasTerm=equality, fromIf=fromIf)
        print(f"Walkbool will return: {line}")
        return generateCode(line)

# TODO: this can probably return if 2 < t3 instead of creating t4 = 2 < t3 and returning that
def walkBool1(root, useTemp=None, hasTerm=None, fromIf=False):
    print("bool1:")
    print("where did the term go")
    print(hasTerm)
    threeAddr.printCode()
    print("is there a temp?")
    print(useTemp)
    compare = root.children[0].type
    print("what's the compare?")
    print(compare)
    # TODO: This fixes one test case. Does this break others?
    # TODO labels should be different if it's an && or an ||
    if hasTerm and fromIf:
        label = threeAddr.addLabel()
        threeAddr.addCode(f"if {hasTerm}{threeAddr.getLastTemp()} goto _")
        if compare == "||":
            print("EXPECT goto stmt")
            threeAddr.expectBackPatch(compare)
            threeAddr.addCode(f"goto {label}")
        elif compare == "&&":
            print("EXPECT goto next if")
            threeAddr.addCode(f"goto _")
            threeAddr.expectBackPatch(compare)
        threeAddr.expectLabel(label)
        hasTerm = None
    if root.children[1].type == "equality":
        print("running walkEquality")
        line = f"{walkEquality(root.children[1])}"
        temp = ""
        new_temp = ""
        tokens = line.split(" ")
        print(tokens)
        if len(tokens) == 1:
            # Ensures addition/subtraction is performed from left to right
            if hasTerm:
                print("yep")
                temp = threeAddr.addTemp()
                print("I RETURNED")
                threeAddr.addCode(f"{temp} = {hasTerm} {compare} {tokens[0]}")
            else:
                print("NO, I RETURNED!")
                return f"{compare} {tokens[0]}"
        # print(tokens)
        print("what's the line that got returned?")
        print(line)
        # If a long line is returned, generate a bunch of temp variables
        if len(tokens) > 2:
            print(f"FROMIF BOOL? {fromIf}")
            if fromIf:
                if not hasTerm and compare == "&&":
                    threeAddr.expectBackPatch(compare)
                label = threeAddr.addLabel()
                threeAddr.addCode(f"if {tokens[0]} {tokens[1]} {tokens[2]} goto {label}")
                threeAddr.expectLabel(label)
                if not hasTerm:
                    if compare == "||": 
                        print("EXPECT goto stmt")
                        # threeAddr.expectBackPatch(compare)
                        threeAddr.addCode(f"goto _")
                        # threeAddr.expectBackPatch(compare)
                    elif compare == "&&":
                        label = threeAddr.addLabel()
                        print("EXPECT goto next if")
                        threeAddr.addCode(f"goto {label}")
                        threeAddr.expectLabel(label)
                        # threeAddr.expectBackPatch(compare)
                        # threeAddr.expectBackPatch(compare)
            else:
                temp = threeAddr.addTemp()
                new_temp = temp
                threeAddr.addCode(f"{temp} = {tokens[0]} {tokens[1]} {tokens[2]}")
                threeAddr.expectLabel(label)
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
            print("figure out why this is being ran")
        #     print(tokens[0])
        #     print(tokens[1])
        #     threeAddr.addCode(f"{new_temp} = {useTemp} {tokens[0]} {tokens[1]}")
        else:
            # Use generated temp from previous steps to ensure actions are performed from left to right
            if useTemp:
                new_temp = threeAddr.addTemp()
                threeAddr.addCode(f"{new_temp} = {useTemp} {compare} {tokens[0]}")
                print("Nah it was me")
                #  todo may not need to return here
                return f"{new_temp}"
            else:
                # TODO what do we do here?
                print("yikes figure out if you need this")
                print(tokens)
        # Recursively run the rest of the bool1s
        if len(root.children) > 2:
            # TODO should i check this here?
            # if hasTerm:
            #     print("Term detected")
            #     threeAddr.addCode(f"{hasTerm} {oper} {new_temp}")
            line = walkBool1(root.children[2], temp, fromIf=fromIf)
            tokens = line.split(" ")
            print(f"new_temp = {new_temp}")
            if len(tokens) == 1:
                new_temp = tokens[0]
            else:
                get_temp = threeAddr.getLastTemp()
                new_temp = threeAddr.addTemp()
                print(f"{new_temp} = {get_temp} {line}")
                threeAddr.addCode(f"{new_temp} = {get_temp} {line}")
            print("WHAT DID THIS RETURN?")
            print(line)
        print("the end of the world")
        return f"{new_temp}"
        # return f"{oper} {new_temp}"

def walkEquality(root, fromIf=False):
    if len(root.children) == 1:
        root = root.children[0]
        if root.type == "relation":
            print("walking relation")
            return walkRelation(root, fromIf)
    else:
        print("What does this return anyway?")
        print(walkRelation(root.children[0]))
        line = f"{walkRelation(root.children[0], fromIf)} {walkEquality1(root.children[1], fromIf)}"
        return generateCode(line)

def walkEquality1(root, useTemp=None, hasTerm=None, fromIf=False):
    print("equality1:")
    print("where did the term go")
    print(hasTerm)
    threeAddr.printCode()
    if root.children[1].type == "relation":
        print("running walkRelation")
        equal = root.children[0].type
        print(f"whats compare? {equal}")
        line = f"{walkRelation(root.children[1], fromIf)}"
        temp = ""
        new_temp = ""
        tokens = line.split(" ")
        if len(tokens) == 1:
            # Ensures addition/subtraction is performed from left to right
            if hasTerm:
                temp = threeAddr.addTemp()
                print("I RETURNED")
                threeAddr.addCode(f"{temp} = {hasTerm} {equal} {tokens[0]}")
            else:
                print("NO, I RETURNED!")
                return f"{equal} {tokens[0]}"
        print("what's the line that got returned?")
        print(line)
        # If a long line is returned, generate a bunch of temp variables
        if len(tokens) > 2:
            print(f"FROMIF EQUALITY? {fromIf}")
            if fromIf:
                label = threeAddr.addLabel()
                threeAddr.addCode(f"if {tokens[0]} {tokens[1]} {tokens[2]} goto {label}")
                threeAddr.expectLabel()
            else:
                temp = threeAddr.addTemp()
                new_temp = temp
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
            print("equality: is this needed?")
        #     print(tokens[0])
        #     print(tokens[1])
        #     threeAddr.addCode(f"{new_temp} = {useTemp} {tokens[0]} {tokens[1]}")
        else:
            # Use generated temp from previous steps to ensure actions are performed from left to right
            if useTemp:
                new_temp = threeAddr.addTemp()
                threeAddr.addCode(f"{new_temp} = {useTemp} {equal} {tokens[0]}")
                print("Nah it was me")
                #  todo may not need to return here
                return f"{new_temp}"
            else:
                print("yikes, do we need? or is this not possible?")
                print(tokens)
                # threeAddr.addCode(f"{new_temp} = {tokens[0]}")
        if len(root.children) > 2:
            line = walkEquality1(root.children[2], temp)
            tokens = line.split(" ")
            print(f"new_temp = {new_temp}")
            if len(tokens) == 1:
                new_temp = tokens[0]
            else:
                get_temp = threeAddr.getLastTemp()
                new_temp = threeAddr.addTemp()
                threeAddr.addCode(f"{new_temp} = {get_temp} {line}")
            print("WHAT DID THIS RETURN?")
            print(line)
        print("the end of the world")
        return f"{new_temp}"
        # return f"{oper} {new_temp}"

def walkRelation(root, fromIf=False):
    if len(root.children) == 1:
        root = root.children[0]
        if root.type == "expr":
            print("walking expr")
            return walkExpr(root)
    else:
        line = f"{walkExpr(root.children[0])} {walkRelation1(root.children[1])}"
        print("walkRelation second case returned:")
        print(line)
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
            term = walkTerm(root.children[0])
            print(f"RECEIVED TERM: {term}")
            line = walkExpr1(root.children[1], hasTerm=term)
            print(f"walkExpr received: {line}")
            return line
    
def walkExpr1(root, useTemp=None, hasTerm=None):
    print("expr1:")
    print("where did the term go")
    print(hasTerm)
    threeAddr.printCode()
    if root.children[1].type == "term":
        print("running walkTerm")
        oper = root.children[0].type
        print(f"whats oper? {oper}")
        line = f"{walkTerm(root.children[1])}"
        temp = ""
        new_temp = ""
        tokens = line.split(" ")
        if len(tokens) == 1:
            # Ensures addition/subtraction is performed from left to right
            if hasTerm:
                temp = threeAddr.addTemp()
                print("I RETURNED")
                print("is this the culprit?")
                print(f"{temp} = {hasTerm} {oper} {tokens[0]}")
                threeAddr.addCode(f"{temp} = {hasTerm} {oper} {tokens[0]}")
            else:
                print("NO, I RETURNED!")
                return f"{oper} {tokens[0]}"
        # print(tokens)
        print("what's the line that got returned?")
        print(line)
        # If a long line is returned, generate a bunch of temp variables
        if len(tokens) > 2:
            temp = threeAddr.addTemp()
            new_temp = temp
            threeAddr.addCode(f"{temp} = {tokens[0]} {tokens[1]} {tokens[2]}")
            i = 3
            while i < len(tokens) - 1:
                new_temp = threeAddr.addTemp()
                token_oper = tokens[i]
                i += 1
                token_value = tokens[i]
                i += 1
                print(f"ADDING: {new_temp} = {temp} {token_oper} {token_value}")
                threeAddr.addCode(f"{new_temp} = {temp} {token_oper} {token_value}")
                temp = new_temp
        # TODO do i need??
        # elif len(tokens) > 1:
        #     print(tokens[0])
        #     print(tokens[1])
        #     threeAddr.addCode(f"{new_temp} = {useTemp} {tokens[0]} {tokens[1]}")
        else:
            # Use generated temp from previous steps to ensure actions are performed from left to right
            if useTemp:
                new_temp = threeAddr.addTemp()
                threeAddr.addCode(f"{new_temp} = {useTemp} {oper} {tokens[0]}")
                print("Nah it was me")
                #  todo may not need to return here
                return f"{new_temp}"
            else:
                print("yikes")
                print(tokens)
                # threeAddr.addCode(f"{new_temp} = {tokens[0]}")
        # Perform any actions that occur after the operations /, //, *, %
        if len(root.children) > 2:
            # TODO should i check this here?
            # if hasTerm:
            #     print("Term detected")
            #     threeAddr.addCode(f"{hasTerm} {oper} {new_temp}")
            line = walkExpr1(root.children[2], temp)
            tokens = line.split(" ")
            print(f"new_temp = {new_temp}")
            if len(tokens) == 1:
                new_temp = tokens[0]
            else:
                print('odsf')
                get_temp = threeAddr.getLastTemp()
                new_temp = threeAddr.addTemp()
                threeAddr.addCode(f"{new_temp} = {get_temp} {line}")
            print("WHAT DID THIS RETURN?")
            print(line)
        return f"{new_temp}"
        # return f"{oper} {new_temp}"

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
            return generateCode(line)

def walkTerm1(root):
    if len(root.children) == 2:
        line = f"{root.children[0].value.value} {walkFactor(root.children[1])}"
    else:
        line = f"{root.children[0].value.value} {walkFactor(root.children[1])} {walkTerm1(root.children[2])}"
    return line

def generateCode(line):
    print(f"CHECKING FOR TEMPS IN LINE: {line}")
    tokens = line.split(" ")
    if len(tokens) > 2:
        temp = threeAddr.addTemp()
        new_temp = temp
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
        return new_temp

def walkFactor(root):
    print("whats the factor?")
    return root.value[0].value

def inter(symbolTable, tree):
    walkTree(tree)

def getThreeAddr():
    threeAddr.cleanUpLabels()
    threeAddr.printCode()
    return threeAddr.getCode()