import re

KEYWORS = {
    'ቁጥር': 'INT', 
    'ባዶ': 'NONE',
    'እውነታ': 'BOOL',
    'ፊደል': 'CHAR',
    'ጽሁፍ': 'STRING',
    'ስብስብ': 'LIST',
    'ከሆነ': 'IF',
    'አለበለዚያ': 'ELSE',
    'እስከሆነ': 'WHILE_1',
    'መልስ': 'RETURN',
    'ፋንክሽን': 'FUNC',
    'ክላስ': 'CLASS',
    'ወይም': 'OR',
    'እና': 'AND',
    'ተቃርኖ': 'NOT',
    'አዲስ': 'NEW',
    'ፍጠር' : 'INIT'
}

INT_T = 'INT'
BOOL_T = 'BOOL'
CHAR_T = 'CHAR'

KEYWORD_T = 'KEYWORD'
IDENTIFIER_T = 'IDENTIFER'

THREE_DOT_T = 'THREE_DOT'
FOUR_DOT_T = 'FOUR_DOT'
TAB_T = 'TAB'
LPARAM_T = 'LPARAM'
RPARAM_T = 'RPARAM'
DOT_T = 'DOT'

EQUAL_T = 'EQUAL'
PLUS_T = 'PLUS'
MINUS_T = 'MINUS'
MULT_T = 'MULT'
DIVIDE_T = 'DIVIDE'
COMMA_T = 'COMMA'

ELIF = 'ደግሞ'
WHILE = 'ድረስ'


NUMS = '0123456789'
ALPHANUMERAL = r'[a-zA-Z\u1200-\u135A0-9_]+'
