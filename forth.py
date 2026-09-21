""" 
Forth interpreter in Python.
"""
from decimal import Decimal

def popnum():
    """ Get a number off the stack. """
    return Decimal(stack.pop())

stack = []
dictionary = {
    # Arithmetic operators
    "+": lambda: stack.append(popnum() + popnum()), 
    "-": lambda: stack.append(popnum() - popnum()), 
    "*": lambda: stack.append(popnum() * popnum()), 
    "/": lambda: stack.append(popnum() / popnum()),

    # Inbuilt debug / quit functions
    "_q": lambda: exit(),
    "_d": lambda: print(dictionary),
    }


def token_index(tokens, to_find):
    for i, x in enumerate(tokens):
        if x == to_find:
            return i
    raise Exception("End delimiter not found")

def process_tokens(tokens):
    """ Process a string and produce an output, with stack manipulation."""
    first_token = tokens[0]
    if first_token == ":":
        code_definition_end = token_index(tokens[2:], ";")+2
        dictionary[tokens[1]] = tokens[2:code_definition_end]
        return tokens[code_definition_end+1:]
    elif first_token.isnumeric():
        stack.append(first_token)
    else:
        found = dictionary[first_token]
        if callable(found):
            found()
        else:
            found_tokens = dictionary[first_token]
            while len(found_tokens):
                found_tokens = process_tokens(found_tokens)
    return tokens[1] if len(tokens) > 1 else []

def repl():
    """ Run in an endless loop of read, eval, print, loop. """
    print("Launching REPL...")
    while True:
        data = input("* ")
        try:
            tokens = data.split(" ")
            while len(tokens):
                tokens = process_tokens(tokens)
            print(stack)
        except Exception as e:
            print(f"ERROR: {e}")
            raise e # Uncomment to use the Python debugger for tracing errors

if __name__ == '__main__':
    """ Try evaluating some expressions."""
    repl()