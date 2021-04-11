import re

# Assembly generation data structures
# TODO do we need to worry about max registers?
class Descriptors:
    def __init__(self):
        MAX_REGISTERS = 16
        self.empty_registers = MAX_REGISTERS
        self.registers = [None] * MAX_REGISTERS
        self.addresses = []
        self.label = ""

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

    def saveLabel(self, label):
        self.label = label

    def getLabel(self):
        label = self.label
        self.label = ""
        return label

# START three-address code to assembly
def generator(symbolTable, threeAddr):
    # Test code:
    # threeAddr = [
    #     "t1 = 2*10",
    #     "t2 = t1 / 11",
    #     "t3 = t2 % 3",
    #     "t4 = 100 + t3",
    #     "a = t4"
    # ]
    three_address_split = []
    for line in threeAddr:
        three_address_split.append(line.strip().split(" "))
    # printIntermediate(three_address)
    # print("===============")
    descriptors = Descriptors()
    assembly = interToAssembly(symbolTable, descriptors, three_address_split)
    printAssembly(assembly)

def interToAssembly(symbolTable, descriptors, three_address):
    assembly = []
    for line in three_address:
        if hasLabel(line):
            descriptors.saveLabel(line[0])
            line = line[1:]
        if isCopy(line):
            # Get registers and load result
            registers = getRegisters(descriptors, line, assembly)
            assembly_line = getLineStart(descriptors)
            assembly_line = assembly_line + f"ST R{registers[0]}, R{registers[1]}"
            assembly.append(assembly_line)
        elif isOperation(line):
            # Get registers and perform requested operation
            registers = getRegisters(descriptors, line, assembly)
            operation = getOperation(line)
            assembly_line = getLineStart(descriptors)
            assembly_line = assembly_line + f"{operation} R{registers[0]}, R{registers[1]}, R{registers[2]}"
            assembly.append(assembly_line)
        elif isIfConditional(line):
            # Get registers and perform subtraction
            registers = getRegisters(descriptors, line, assembly)
            compare = getCompare(line)
            assembly_line = getLineStart(descriptors)
            assembly_line = assembly_line + f"SUB R{registers[0]}, R{registers[0]}, R{registers[1]}"
            assembly.append(assembly_line)
            # Goto branch if condition is satisfied
            assembly_line = getLineStart(descriptors)
            assembly_line = assembly_line + f"{compare} R{registers[0]}, {line[-1]}"
            assembly.append(assembly_line)
            # print(line)
        elif isGoto(line):
            assembly_line = getLineStart(descriptors)
            # TODO what is the exact label for a nonconditional branch?
            assembly_line = assembly_line + f"B {line[-1]}"
            assembly.append(assembly_line)
        elif isPrint(line):
            assembly_line = getLineStart(descriptors)
            # TODO how do we actually print? :S
            assembly_line = assembly_line + f"CALL print, {line[-1]}"
            assembly.append(assembly_line)

    return assembly

# For testing: Prints the generated assembly code
def printAssembly(assembly):
    for line in assembly:
        print(line)

# Given a line of three-address code, for each variable returns its register index
# If variable is not already in a register, it will be loaded into to some register,
# and the assembly code will be updated to reflect the load
def getRegisters(descriptors, line, assembly):
    keywords = ["if", "goto"]
    registers = []
    for token in line:
        if token not in keywords and token.isalnum():
            register_index = descriptors.getRegisterWithValue(token)
            if register_index == -1:
                assembly_line = getLineStart(descriptors)
                register_index = descriptors.insertIntoRegister(register_index, token)
                assembly_line = assembly_line + f"LD R{register_index}, {token}"
                assembly.append(assembly_line)
            registers.append(register_index)
        elif token == "goto":
            break
    return registers

def getLineStart(descriptors):
    label = descriptors.getLabel()
    if label != "":
        return f"{label} "
    else:
        return "    "
    

def hasLabel(line):
    return re.match("L[0-9]+:", line[0])

# Returns true if the three-address code given is an operation e.g. a + b = c
def isOperation(line):
    return len(line) == 5 and line[0].isalnum() and line[2].isalnum() and line[4].isalnum()

# Returns true if the three-address code given copies e.g. x = y
def isCopy(line):
    return len(line) == 3 and line[0].isalnum() and line[1] == "=" and line[2].isalnum()

def isIfConditional(line):
    return line[0] == "if"

def isGoto(line):
    return line[0] == "goto"

def isPrint(line):
    return line[0] == "call"

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

def getCompare(line):
    comparisons = {
        "<": "BLTZ",
        "<=": "BLEZ",
        ">": "BGTZ",
        ">=": "BGEZ",
        "==": "BEQZ",
        "!=": "BNEZ",
    }
    return comparisons[line[2]]