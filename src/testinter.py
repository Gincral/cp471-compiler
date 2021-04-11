from os import error
import sys
from lexer import lexer
from symbol import SymbolTable
from symbol import SymbolTable, Data
from parse import parse
from inter import inter, getThreeAddr, clearCode
from generator import generator

import unittest

class TestStringMethods(unittest.TestCase):
    # Test Case 1
    def test1(self):
        symbolTable = SymbolTable()
        line = "def number a = 100 + 2*10 // 11 % 3;"
        tokenList = lexer(line.strip())
        if not (tokenList): raise Exception("lexer Error")
        par = parse(symbolTable, tokenList)
        if not (par): raise Exception("parser Error")
        inter(symbolTable, par)
        threeAddr = getThreeAddr()
        self.assertEqual(threeAddr, ['    t1 = 2 * 10', '    t2 = t1 // 11', '    t3 = t2 % 3', '    t4 = 100 + t3', '    a = t4'])

    def test2(self):
        clearCode()
        symbolTable = SymbolTable()
        line = "def number s = 1 * 5 + 6;"
        tokenList = lexer(line.strip())
        if not (tokenList): raise Exception("lexer Error")
        par = parse(symbolTable, tokenList)
        if not (par): raise Exception("parser Error")
        inter(symbolTable, par)
        threeAddr = getThreeAddr()
        self.assertEqual(threeAddr, ['    t1 = 1 * 5', '    t2 = t1 + 6', '    s = t2'])

    # Test Case 2
    def test3(self):
        clearCode()
        symbolTable = SymbolTable()
        line = "if (2 < 5 + 6 * 3 - 8): { def number y = 0; } else:{ def number z = 0; }"
        tokenList = lexer(line.strip())
        if not (tokenList): raise Exception("lexer Error")
        par = parse(symbolTable, tokenList)
        if not (par): raise Exception("parser Error")
        inter(symbolTable, par)
        threeAddr = getThreeAddr()
        self.assertEqual(threeAddr, ['    t1 = 6 * 3', '    t2 = 5 + t1', '    t3 = t2 - 8', '    if 2 < t3 goto L1', '    goto L2', 'L1: y = 0', 'L2: z = 0'])

    # test1.txt
    def test4(self):
        clearCode()
        symbolTable = SymbolTable()
        line = "if (3 * 2 <= 5 + 6 * 3 - 8): { def number y = 0; } else:{ def number z = 0; }"
        tokenList = lexer(line.strip())
        if not (tokenList): raise Exception("lexer Error")
        par = parse(symbolTable, tokenList)
        if not (par): raise Exception("parser Error")
        inter(symbolTable, par)
        threeAddr = getThreeAddr()
        self.assertEqual(threeAddr, ['    t1 = 3 * 2', '    t2 = 6 * 3', '    t3 = 5 + t2', '    t4 = t3 - 8', '    if t1 <= t4 goto L1', '    goto L2', 'L1: y = 0', 'L2: z = 0'])

    # Test Case 3
    def test5(self):
        clearCode()
        symbolTable = SymbolTable()
        line = "if (x < a+b || x > c && x<=d):{ def number y = 0; } else:{ if (x>=e):{ def number z = 0; } }"
        tokenList = lexer(line.strip())
        if not (tokenList): raise Exception("lexer Error")
        par = parse(symbolTable, tokenList)
        if not (par): raise Exception("parser Error")
        inter(symbolTable, par)
        threeAddr = getThreeAddr()
        self.assertEqual(threeAddr, ['    t1 = a + b', '    if x < t1 goto L2', '    goto L1', 'L1: if x > c goto L2', '    goto L4', 'L2: if x <= d goto L3', '    goto L4', 'L3: y = 0', 'L4: if x >= e goto L5', 'L5: z = 0'])

    def test6(self):
        clearCode()
        symbolTable = SymbolTable()
        line = "def number b = 5 + 302 * 2 + 6 // 2 + 4;"
        tokenList = lexer(line.strip())
        if not (tokenList): raise Exception("lexer Error")
        par = parse(symbolTable, tokenList)
        if not (par): raise Exception("parser Error")
        inter(symbolTable, par)
        threeAddr = getThreeAddr()
        self.assertEqual(threeAddr, ['    t1 = 302 * 2', '    t2 = 5 + t1', '    t3 = 6 // 2', '    t4 = t2 + t3', '    t5 = t4 + 4', '    b = t5'])

    def test7(self):
        clearCode()
        symbolTable = SymbolTable()
        line = "def boolean result = TRUE || FALSE && TRUE;"
        tokenList = lexer(line.strip())
        if not (tokenList): raise Exception("lexer Error")
        par = parse(symbolTable, tokenList)
        if not (par): raise Exception("parser Error")
        inter(symbolTable, par)
        threeAddr = getThreeAddr()
        print(threeAddr)
        self.assertEqual(threeAddr, ['    t1 = TRUE || FALSE', '    t2 = t1 && TRUE', '    result = t2'])

    # test3.txt
    def test8(self):
        clearCode()
        symbolTable = SymbolTable()
        lines = [
            "def boolean result = TRUE || FALSE && TRUE;",
            "result = FALSE && TRUE;",
            "print(result);"
        ]
        for line in lines:
            tokenList = lexer(line.strip())
            if not (tokenList): raise Exception("lexer Error")
            par = parse(symbolTable, tokenList)
            if not (par): raise Exception("parser Error")
            inter(symbolTable, par)
            threeAddr = getThreeAddr()
        print(threeAddr)
        self.assertEqual(threeAddr, ['    t1 = TRUE || FALSE', '    t2 = t1 && TRUE', '    result = t2', '    t3 = FALSE && TRUE', '    result = t3', '    call print, result'])

if __name__ == '__main__':
    unittest.main()