#import re

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
POWER_T = 'POWER'
COMMA_T = 'COMMA'

EOF_T = 'EOF'

ELIF = 'ደግሞ'
WHILE = 'ድረስ'


NUMS = '0123456789'
ALPHANUMERAL = r'[a-zA-Z\u1200-\u135A0-9_]+'


#####################################################################
## Error Message
#####################################################################

ILLEGAL_CHARACTER_ERROR = 'የማይታወቅ ካራክተር አለ።'
ILLEGAL_SYNTAX_ERROR = 'የተሰበረ ህግ አለ።'
RUNTIME_ERROR = 'ያልተጠበቀ ስተት አለ።'

RPARAM_MISSING_ERROR = 'መዝጊያ ቅንፍ ")" ተረስታል'
INT_MISSING_ERROR = 'ቁጥር ተረስታ'
DIVISION_BY_ZERO_ERROR = 'በዘሮ ማካፈል አይቻልም'