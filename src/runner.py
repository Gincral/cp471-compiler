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

# Assembly generation data structures
class Register:
    def __init__(self):
        self.variable = None

class Descriptors:
    def __init__(self):
        MAX_REGISTERS = 16
        self.empty_registers = MAX_REGISTERS
        self.registers = [None] * MAX_REGISTERS
        self.addresses = []

    def getRegisterWithValue(self, variable):
        if variable in self.registers:
            return self.registers.index(variable)
        return -1

    def insertIntoRegister(self, index, variable):
        index = 0
        while self.registers[index] is not None:
            index += 1
        self.registers[index] = variable
        self.empty_registers -= 1
        return index

class ThreeAddressCode:
    def __init__(self):
        self.code = []
        self.labels = 0
        self.temps = 0

    def addCode(self, line):
        self.code.append(line)

    def getCode(self):
        return self.code

    def printCode(self):
        print("Intermediate Code:")
        print(self.code)

    def addLabel(self):
        self.labels += 1
        return f"L{self.labels}"

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
    root = root.children[0]
    if root.type == "dec":
        print("we're at the dec")
        walkDec(root)
    elif root.type == "assign":
        print("we're at the assign")
        walkAssign(root)
    elif root.type == "ifstmt":
        print("we're at the ifstmt")
        walkIfStmt(root)
        if len(root.children) > 1:
            label = threeAddr.addLabel()
            threeAddr.addCode(f"goto {label}")
            for child in root.children:
                if child.type == "stmt":
                    walkStmt(child)

def walkDec(root):
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
            return line


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
    print(root.children[0].type)
    print(root.children[1].type)
    if root.children[1].type == "equality":
        print("we've got an equality")
        compare = root.children[0].value.value
        line = f"{walkEquality(root.children[1])}"
        print(line)
        # tokens = line.split(" ")
        # print(tokens)
        # temp = threeAddr.addTemp()
        # new_temp = temp
        # if len(tokens) > 2:
        #     threeAddr.addCode(f"{temp} = {tokens[0]} {tokens[1]} {tokens[2]}")
        #     i = 3
        #     while i < len(tokens) - 1:
        #         print(i)
        #         new_temp = threeAddr.addTemp()
        #         token_oper = tokens[i]
        #         i += 1
        #         token_value = tokens[i]
        #         i += 1
        #         threeAddr.addCode(f"{new_temp} = {temp} {token_oper} {token_value}")
        #         temp = new_temp
        # else:
        #     threeAddr.addCode(f"{temp} = {tokens[0]}")
        # threeAddr.printCode()
        # return f"{oper} {new_temp}"


def walkEquality(root):
    root = root.children[0]
    if root.type == "relation":
        print("we're at the relation")
        return walkRelation(root)

def walkRelation(root):
    if len(root.children) == 1:
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
        print("haihdasd")

def walkCompar(root):
    print("whats the comparison?")
    print(root.value.value)
    return root.value.value

def walkExpr(root):
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
    # TODO
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
            threeAddr.printCode()
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

#  Help
# t1 = 2*10
# t2 = t1 / 11
# t3 = t2 % 3
# t4 = 100 + t3
# a = t4

def runner(symbolTable, tree):
    inter = []
    print(tree.value[0].value)
    walkTree(tree)
    three_address_split = []
    for line in threeAddr.getCode():
        three_address_split.append(line.split(" "))
    
    # # Test - this works so far
    # three_address = [
    #     ["t1", "=", "b", "*", "c"],
    #     ["t2", "=", "t1", "/", "d"],
    #     ["t3", "=", "t2", "%", "e"],
    #     ["t4", "=", "a", "+", "t3"],
    #     ["num", "=", "t4"]
    # ]
    # three_address = [
    #     ["t1", "=", "a", "+", "b"],
    #     ["if", "x", "<", "t1", "goto", "L2"],
    #     ["goto", "L1"],
    #     ["L1:", "if", "x", ">", "c", "goto", "L2"],
    #     ["goto", "L4"],
    #     ["L2:", "if", "x", "<=", "d", "goto", "L3"],
    #     ["goto", "L4"],
    #     ["L3:", "y", "=", "0"],
    #     ["L4:", "if", "x", ">=", "e", "goto", "L5"],
    #     ["L5:", "z", "=", "0"]
    # ]
    # printIntermediate(three_address)
    # print("===============")
    descriptors = Descriptors()
    assembly = interToAssembly(symbolTable, descriptors, three_address_split)
    printAssembly(assembly)

# START: generate three-address code


# For testing: Prints the generated three-address code 
def printIntermediate(three_address):
    for line in three_address:
        three_address_code = " "
        print(three_address_code.join(line))

# START three-address code to assembly

def interToAssembly(symbolTable, descriptors, three_address):
    assembly = []
    for line in three_address:
        if isCopy(line):
            registers = getRegisters(descriptors, line, assembly)
            assembly.append(f"ST R{registers[0]}, R{registers[1]}")
        elif isOperation(line):
            registers = getRegisters(descriptors, line, assembly)
            operation = getOperation(line)
            assembly.append(f"{operation} R{registers[0]}, R{registers[1]}, R{registers[2]}")
    return assembly

# For testing: Prints the generated assembly code
def printAssembly(assembly):
    for line in assembly:
        print(line)

# Given a line of three-address code, for each variable returns its register index
# If variable is not already in a register, it will be loaded into to some register,
# and the assembly code will be updated to reflect the load
def getRegisters(descriptors, line, assembly):
    registers = []
    for token in line:
        if token.isalnum():
            register_index = descriptors.getRegisterWithValue(token)
            if register_index == -1:
                register_index = descriptors.insertIntoRegister(register_index, token)
                assembly_line = f"LD R{register_index}, {token}"

                assembly.append(assembly_line)
            registers.append(register_index)

    return registers

# Returns true if the three-address code given is an operation e.g. a + b = c
def isOperation(line):
    return len(line) == 5 and line[0].isalnum() and line[2].isalnum() and line[4].isalnum()

# Returns true if the three-address code given copies e.g. x = y
def isCopy(line):
    return len(line) == 3 and line[0].isalnum() and line[1] == "=" and line[2].isalnum()

# Returns the assembly operation for the provided operation symbol e.g. given "+", return "ADD"
def getOperation(line):
    operations = {
        "+": "ADD",
        "-": "SUB",
        "*": "MUL",
        "/": "DIV",
        "%": "MOD",
        "//": "IDIV"
    }
    return operations[line[3]]

def isIfConditional(line):
    return 

def isElseConditional(line):
    return