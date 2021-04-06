import re

# Intermediate (three-address) code data structures
class Node:
    def __init__(self):
        Node.labels += 1
        self.label = f"L{Node.labels}"
        return

    def getLabel():
        return self.label

Node.labels = 0

# class Expr:
#     def __init__(self, op, exprType):
#         self.op = op
#         self.type = exprType

#     def gen():
#         return
    
#     def reduceExpr():
#         return

#     def jumping():
#         return

#     def jumps(condition, ifTrue, ifFalse):
#         return [f"if {condition} then {iftrue}", f"goto {ifFalse}"]

# class Id(expr.Expr):
#     def __init__(self, op, exprType, offset):
#         Expr.__init__(self, op, exprType)
#         self.offset = offset

# class Op(expr.Expr):

#     def __init__(self, op, exprType):
#         Expr.__init__(self, op, exprType)
#         self.offset = offset
    
#     def reduceExpr():
#         x = Expr.gen()
#         Op.tempLabels += 1
# Op.tempLabels = 0 

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


def runner(symbolTable):
    # TODO get the intermediate code generated
    # Test
    three_address = [
        ["t1", "=", "b", "*", "c"],
        ["t2", "=", "t1", "/", "d"],
        ["t3", "=", "t2", "%", "e"],
        ["t4", "=", "a", "+", "t3"],
        ["num", "=", "t4"]
    ]
    three_address = [
        ["t1", "=", "a", "+", "b"],
        ["if", "x", "<", "t1", "goto", "L2"],
        ["goto", "L1"],
        ["L1:", "if", "x", ">", "c", "goto", "L2"],
        ["goto", "L4"],
        ["L2:", "if", "x", "<=", "d", "goto", "L3"],
        ["goto", "L4"],
        ["L3:", "y", "=", "0"],
        ["L4:", "if", "x", ">=", "e", "goto", "L5"],
        ["L5:", "z", "=", "0"]
    ]
    printIntermediate(three_address)
    print("===============")
    descriptors = Descriptors()
    assembly = interToAssembly(symbolTable, descriptors, three_address)
    printAssembly(assembly)

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

# For testing: Prints the generated three-address code 
def printIntermediate(three_address):
    for line in three_address:
        three_address_code = " "
        print(three_address_code.join(line))

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
        "%": "MOD"
    }
    return operations[line[3]]

def isIfConditional(line):
    return 

def isElseConditional(line):
    return