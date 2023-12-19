Autor: Hailemichael Alemneh

CS 191: Senior Project
Ahadu - Amharic Object Oriented Language

Ahadu is an Amharic (serves as the official working language of the Ethiopian 
federal government. As of 2018, it has over 32.4 million mother-tongue speakers 
and more than 25.1 million second language speakers in 2019.) based programming 
language I developed for computer programming education purposes. Ahadu aims to 
serve as an educational tool for Amharic speaking individuals interested in 
learning programming. It also aims to introduce Amharic speakers previously not 
exposed to the concepts of programming or discouraged from learning programming 
due to language barriers to computer programming. And as such, it is designed 
with beginner programmers in mind. It is structured to be comprehensible for 
Amharic speakers by mimicking Amharic sentence structures. The programming 
language is designed and built with the assumption the user knows little to no 
English. This means all the reserved keywords are in Amharic. These are not 
mere translations of the English keywords from other programming languages but
words that are selected to represent the concept of the keywords and be as 
easily accessible and comprehensible to Amharic speakers as possible. Variable 
names, strings, and so on will also support the Geez Fidel letters in which 
Amharic is written in, in addition to English letters. Error messages outputted 
by the interpreter will also be in Amharic. 

This repo contains the interpreter for Ahadu.

/example - some example Ahadu code

/resources 
- constants.py constants used through out the code
- error.py defines the different error types and how they are printed
- nodes.py defines the node class the parser builds an ast out of
- type.py defines the different types support by Ahadu and the operation 
allowed on them. These types are DefaultType, Number, String, Array, Function,
Class, and Object.

/src
- lexer.py - contains the Lexer class defintion and lexer method which take the
code input as text and convert it to a list of tokens. The file also defines 
the Token class.
- parser_.py - contains the Parser class defintion and parse methods that parse 
the list of tokens outputted by the lexer method into an AST made of nodes 
defined in node.py
- interpreter.py - contains the Interpreter class defintion and visit method for
each node type from the parser execute the code associated with each node. It 
also contains the defintion for the Context class which contains the 
Symbol_Table for the context of execution. The Symbol_Table class is the 
dictionary that keeps track of the variables, classes, objects, and functions
defined through out the code.

/web contains the web interface for writing Ahadu code and viewing the results

run.py contains the code to run the whole interpreter when a file is passed to
it as an argument.