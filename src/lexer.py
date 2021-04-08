import re

LEXEMES = ['def', 'string', 'boolean', 'number', 'type', 'if', 'else', 'and','&&',
 'or', '||', '+', '-', '*', '/', '//', '%', '^', '=', '==', '!=', '<', '>', '<=', '>=', '(', ')', ':', '{', '}', 'print', ';']
BOOLEANS = ['TRUE', 'FALSE', 'NULL']

class Token:
    def __int__(self, type, value):
        self.type = type #types: lex, num, str, boo, id
        self.value = value

def lexer(line):
    lists = []
    line = line[:-1] #remove /n
    stack = ''
    print("line: ",line)
    while line:
        stack += line[0]
        line = line[1:]
        if stack == ' ': #remove space
            stack = ''
        elif stack == '"': # check if its string
                token = Token()
                token.type = 'string'
                try:
                    while line[0] != '"':
                        stack += line[0]
                        line = line[1:]
                    stack += line[0]
                    line = line[1:]
                except Exception:
                    print("missing quote")
                    return False
                token.value = stack
                lists.append(token)
                stack = ''
                print('str: ', token.value)
        elif (stack in LEXEMES) and (not line or not(stack+line[0] in LEXEMES)): # check if its lexmes
            token = Token()
            token.type = 'lex'
            token.value = stack
            lists.append(token)
            stack = ''
            print('lex: ', token.value)
        elif stack in BOOLEANS: # check if its boolean
            token = Token()
            token.type = 'boolean'
            token.value = stack
            lists.append(token)
            stack = ''
            print('boo: ', token.value)
        elif isnumber(stack): #check if its numbers
            token = Token()
            token.type = 'number'
            while line and (line[0]=='.' or isnumber(line[0])):
                stack += line[0]
                line = line[1:]
            if not isnumber(stack):
                print("number is not correct")
                return False
            token.value = stack
            lists.append(token)
            stack = ''
            print('num: ', token.value)
        elif len(stack) and( not line or line[0]==" " or line[0] in LEXEMES or line[:2] in LEXEMES ) : # check if its id
            token = Token()
            token.type = 'id'
            if not bool(re.match("^[A-Za-z0-9_-]*$", stack)):
                print("id is invalid")
                return False
            token.value = stack
            lists.append(token)
            stack = ''
            print('id: ', token.value)

    if (lists[-1].value != ';') and (lists[-1].value != '{') and (lists[-1].value != '}'): # line should only be end with ;,{,}
        print("End of File Error")
        return False

    return lists

def isnumber(value):
    try:
        float(value)
        return True
    except Exception:
        return False
