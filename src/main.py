from os import error
import sys
from lexer import lexer
from symbol import SymbolTable
# from .inter import *
# from .parser import *



def main():
    input_file_address= sys.argv[1]
    output_file_address= sys.argv[2]
    input_file_address = "input/input.txt"
    output_file_address = "output/result.txt"

    input_file = open(input_file_address, "r")
    output_file = open(output_file_address, "w")

    symbolTable = new SymbolTable()
    lexemList = lexer(input_file)

    input_file.close()
    output_file.close()

	
	# symbol = new symbol()
	# parser = new parser(lex, symbol, input_file_address, output_file_address)
	# parser.start()


if __name__ == "__main__":
    main()