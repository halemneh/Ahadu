#import re


BOOL_T = 'BOOL'
INT_T = 'INT'
BOOL_T = 'BOOL'
CHAR_T = 'CHAR'

KEYWORD_T = 'KEYWORD'
IDENTIFIER_T = 'IDENTIFIER'

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

LT_T = 'LT'
LTE_T = 'LTE'
GT_T = 'GT'
GTE_T = 'GTE'
EQ_T = 'EQUVALENT'
NEQ_T = 'NEQUAL'

AND_T ='AND'
NOT_T = 'NOT'
OR_T = 'OR'

TRUE_T = 'TRUE'
FALSE_T = 'FALSE'

NEWLINE_T = 'NEWLINE'
EOF_T = 'EOF'

ELIF = 'ደግሞ'
WHILE = 'ድረስ'

KEYWORS = {
    'ቁጥር': INT_T, 
    'ባዶ': 'NONE',
    'እውነታ': BOOL_T,
    'ፊደል': 'CHAR',
    'ጽሁፍ': 'STRING',
    'ስብስብ': 'LIST',
    'ከሆነ': 'IF',
    'አለበለዚያ': 'ELSE',
    'እስከሆነ': 'WHILE_1',
    'መልስ': 'RETURN',
    'ፋንክሽን': 'FUNC',
    'ክላስ': 'CLASS',
    'ወይም': OR_T,
    'እና': AND_T,
    'ተቃርኖ': NOT_T,
    'አዲስ': 'NEW',
    'ፍጠር' : 'INIT',
    'እውነት' : TRUE_T,
    'ሀሰት' : FALSE_T
}

NUMS = '0123456789'
ALPHANUMERAL = r'[a-zA-Z\u1200-\u135A0-9_]+'


#####################################################################
## Error Message
#####################################################################

ILLEGAL_CHARACTER_ERROR = 'የማይታወቅ ካራክተር አለ።'
ILLEGAL_SYNTAX_ERROR = 'የተሰበረ ህግ አለ።'
RUNTIME_ERROR = 'ያልተጠበቀ ስተት አለ።'

UNKNOWN_CHARACTER_ERROR = 'የማይታወቅ ካራክተር አለ።'
INDENTATION_ERROR = ''
RPARAM_MISSING_ERROR = 'መዝጊያ ቅንፍ ")" ተረስታል'
INT_MISSING_ERROR = 'ቁጥር ተረስታ'
DIVISION_BY_ZERO_ERROR = 'በዘሮ ማካፈል አይቻልም'
EXPECTED_IDENTIFIER = 'Identifier Expected'
EXPECTED_EQUALS = 'equals sign expected'
UNDEFINED_IDENTIFIER = 'undefined Variable'