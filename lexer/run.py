from lexer import Lexer

with open("sample.txt") as file:
    text = file.read()

tokens = Lexer(text).lexer()

for i in range(len(tokens)):
    print(tokens[i])