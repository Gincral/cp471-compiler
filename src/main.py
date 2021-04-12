from os import error
import sys
from lexer import lexer
from symbol import SymbolTable
from symbol import SymbolTable, Data
from parse import parse
from inter import inter, getThreeAddr
from generator import generator


def main():
    input_file_address= sys.argv[1]
    output_file_address= sys.argv[2]

    input_file = open(input_file_address, "r")
    output_file = open(output_file_address, "w")

    symbolTable = SymbolTable()
    line = input_file.readline()

    while line:
        while line.replace(" ", "") == "\n": line = input_file.readline()
        print("=====================")
        print("Lexer: ")
        tokenList = lexer(line.strip())
        if not (tokenList): raise Exception("lexer Error")

        print("=====================")
        print("Parser: ")
        par = parse(symbolTable, tokenList)
        if not (par): raise Exception("parser Error")
        
        print("=====================")
        print("Symbol Table: ")
        symbolTable.printTable()

        print("=====================")
        inter(symbolTable, par)
        line = input_file.readline()
        print("=====================")

    threeAddr = getThreeAddr()
    print("=====================")
    assembly = generator(symbolTable, threeAddr, )

    print("======================-------------------------------------------------------------------")
    print("Symbol Table: ")
    symbolTable.printTable()

    for line in assembly:
        output_file.write(line+'\n')

    input_file.close()
    output_file.close()


if __name__ == "__main__":
    main()