# =======================================================================================
# Token types and values 
# =======================================================================================

BOOL_T = 'BOOL'
INT_T = 'INT'
BOOL_T = 'BOOL'
CHAR_T = 'CHAR'
STRING_T = 'STRING'
KEYWORD_T = 'KEYWORD'
IDENTIFIER_T = 'IDENTIFIER'
THREE_DOT_T = 'THREE_DOT'
FOUR_DOT_T = 'FOUR_DOT'
TAB_T = 'TAB'
LPARAM_T = 'LPARAM'
RPARAM_T = 'RPARAM'
LBRACKET_T = 'LBRACKET'
RBRACKET_T = 'RBRACKET'
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
AT_T = 'AT'
SLICE_T = 'SLICE'
CALL_T = 'CALL'
TRUE_T = 'TRUE'
FALSE_T = 'FALSE'
NEWLINE_T = 'NEWLINE'
EOF_T = 'EOF'
IF_T = 'IF'
ELIF_T = 'ELIF'
ELSE_T = 'ELSE'
WHILE_T = 'WHILE'
ELIF = 'ደግሞ'
WHILE = 'ድረስ'
THEN_T = 'THEN'
COLON_T = 'COLON'
ELIF_START_T = 'ELSE_START'
FUNC_T = 'FUNC'
RETURN_T = 'RETURN'
INIT_T = 'INIT'
CLASS_T = 'CLASS'
PRINT_T = 'PRINT'
JOIN_T = 'JOIN'
DELETE_T = 'DELETE'

KEYWORS = {
    'ቁጥር': INT_T, 
    'ባዶ': 'NONE',
    'እውነታ': BOOL_T,
    'ፊደል': 'CHAR',
    'ጽሁፍ': 'STRING',
    'ስብስብ': 'LIST',
    'አዲስ': 'NEW',
    'ከሆነ': IF_T,
    'ከሖነ': IF_T,
    'ከኆነ': IF_T,
    'አለበለዚያ': ELSE_T,
    'ኣለበለዚያ': ELSE_T,
    'ዓለበለዚያ': ELSE_T,
    'ዐለበለዚያ': ELSE_T,
    'ግን' : ELIF_START_T,
    'እስከሆነ': WHILE_T,
    'እስከሖነ': WHILE_T,
    'እስከኆነ': WHILE_T,
    'ዕስከሆነ': WHILE_T,
    'ዕስከሖነ': WHILE_T,
    'ዕስከኆነ': WHILE_T,
    'ተመላሽ': RETURN_T,
    'ፋንክሽን': FUNC_T,
    'ክላስ': CLASS_T,
    'ወይም': OR_T,
    'እና': AND_T,
    'ዕና': AND_T,
    'ተቃርኖ': NOT_T,
    'ፍጠር' : INIT_T,
    'ጻፍ': PRINT_T,
    'ፃፍ': PRINT_T,
    'አዋህድ': JOIN_T,
    'ሰርዝ': DELETE_T,
    'ሠርዝ': DELETE_T
}

BUILT_IN_FUNCS = (PRINT_T, JOIN_T, DELETE_T)

# =======================================================================================
# Error types and messages 
# =======================================================================================

ILLEGAL_CHARACTER_ERROR = 'የማይታወቅ ካራክተር አለ።'
ILLEGAL_SYNTAX_ERROR = 'የተሰበረ ህግ አለ።'
RUNTIME_ERROR = 'ያልተጠበቀ ስተት አለ።'

UNKNOWN_CHARACTER_ERROR = 'የማይታወቅ ካራክተር አለ።'
INDENTATION_ERROR = 'Indentation Error'
RPARAM_MISSING_ERROR = 'መዝጊያ ቅንፍ ")" ተረስታል'
RBRACKET_MISSING_ERROR = 'Missing ]'
INT_MISSING_ERROR = 'ቁጥር ተረስታ'
DIVISION_BY_ZERO_ERROR = 'በዘሮ ማካፈል አይቻልም'
EXPECTED_IDENTIFIER = 'Identifier Expected'
EXPECTED_EQUALS = 'equals sign expected'
UNDEFINED_IDENTIFIER = 'undefined Variable'
ILLEGAL_OPERATION = ''
INDEX_OUT_OF_BOUNDS = 'Index ou of bounds'
NO_OF_ARGS_PASSED = ''

# =======================================================================================
# Other constants
# =======================================================================================
""" Other Constants for lexer.py"""
NUMS = '0123456789'
ALPHANUMERAL = r'[a-zA-Z\u1200-\u135A0-9_]+'
ESCAPE = {'n': '\n', 't': '\t'}