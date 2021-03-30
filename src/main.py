from os import error
import sys
from lexer import lexer
from symbol import SymbolTable
from parser import parser



def main():
    input_file_address= sys.argv[1]
    output_file_address= sys.argv[2]
    input_file_address = "input/input.txt"
    output_file_address = "output/result.txt"

    input_file = open(input_file_address, "r")
    output_file = open(output_file_address, "w")

    symbolTable = SymbolTable()
    line = input_file.readline()

    # while line:
    tokenList = lexer(line)
    par = parser(symbolTable, tokenList)
        # line = input_file.readline()
        # print("=====================")

    input_file.close()
    output_file.close()

	
	# symbol = new symbol()
	# parser = new parser(lex, symbol, input_file_address, output_file_address)
	# parser.start()


if __name__ == "__main__":
    main()