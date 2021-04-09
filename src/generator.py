# Assembly generation data structures
# TODO do we need to worry about max registers?
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

# START three-address code to assembly
def generator(symbolTable, threeAddr):
    # Test code:
    threeAddr = [
        "t1 = 2*10",
        "t2 = t1 / 11",
        "t3 = t2 % 3",
        "t4 = 100 + t3",
        "a = t4"
    ]
    three_address_split = []
    for line in threeAddr:
        three_address_split.append(line.split(" "))
    # printIntermediate(three_address)
    # print("===============")
    descriptors = Descriptors()
    assembly = interToAssembly(symbolTable, descriptors, three_address_split)
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