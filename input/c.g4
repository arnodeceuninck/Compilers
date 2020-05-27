grammar c;

start_rule: (include)? operation_sequence;

include: '#include <stdio.h>';

operation_sequence: (operation SEMICOLON | function |  if_statement | for_statement | while_statement | scope)*;

scope: LEFT_CURLY_BRACE operation_sequence RIGHT_CURLY_BRACE;

function: function_declaration SEMICOLON | function_definition;

function_definition: function_declaration scope;

function_declaration: type_ var=VAR_NAME LEFT_ROUND_BRACE argument_list RIGHT_ROUND_BRACE;

type_: (int_=INT_TYPE|float_=FLOAT_TYPE|char_=CHAR_TYPE|void_=VOID);

variable_declaration: ((const_=CONST)? declaration=type_) variable_use;  // TODO: int f[0](){} shouldn't be allowed.

variable_use: (pointer)* var=VAR_NAME (array=array_index)?;

array_index: LEFT_SQUARE_BRACE index=operation_logic_or RIGHT_SQUARE_BRACE;

pointer: MULT;

function_use: var=VAR_NAME LEFT_ROUND_BRACE use_argument_list RIGHT_ROUND_BRACE;

use_argument_list: (operation_logic_or)?(COMMA operation_logic_or)*;

argument_list: (variable_declaration)?(COMMA variable_declaration)*;

operation: (assignment | operation_logic_or | return_op);

if_statement: IF LEFT_ROUND_BRACE condition=operation_logic_or RIGHT_ROUND_BRACE scope (else_statement)?;

else_statement: ELSE scope;

while_statement: WHILE LEFT_ROUND_BRACE condition=operation_logic_or RIGHT_ROUND_BRACE scope;

for_statement: FOR LEFT_ROUND_BRACE (assignment | operation_logic_or) SEMICOLON (assignment | operation_logic_or) SEMICOLON (assignment |operation_logic_or) RIGHT_ROUND_BRACE scope;

assignment: variable_declaration | assign; // Must be a difference between them to prevent ambiguity x; (declaration or operation_logic_or?)

assign: lvalue ASSIGN operation_logic_or;

lvalue: variable_declaration | variable_use;

operation_logic_or: left=operation_logic_or lor=LOGIC_OR right=operation_logic_and
                  | operation_logic_and;

operation_logic_and: left=operation_logic_and land=LOGIC_AND right=operation_compare_eq_neq
                   | operation_compare_eq_neq;

operation_compare_eq_neq: left=operation_compare_eq_neq (eq=EQUAL|neq=NOT_EQUAL) right=operation_compare_leq_geq_l_g
                        | operation_compare_leq_geq_l_g;

operation_compare_leq_geq_l_g: left=operation_compare_leq_geq_l_g (gt=GREATER_THAN|lt=LESS_THAN|leq=LESS_THAN_OR_EQUAL|geq=GREATER_THAN_OR_EQUAL) right=operation_plus_minus
                             | operation_plus_minus;

operation_plus_minus: left=operation_plus_minus (plus=PLUS|minus=MINUS) right=operation_mult_div
                    | operation_mult_div;

operation_mult_div: left=operation_mult_div (mult=MULT|div=DIV|mod=MOD) right=operation_unary_plus_minus_not
                  | operation_unary_plus_minus_not;

operation_unary_plus_minus_not: pp=PLUS_PLUS right=operation_unary_plus_minus_not
                              | mm=MIN_MIN right=operation_unary_plus_minus_not
                              | plus=PLUS right=operation_unary_plus_minus_not
                              | minus=MINUS right=operation_unary_plus_minus_not
                              | not_=NOT right=operation_unary_plus_minus_not
//                              | rref=MULT right=operation_unary_plus_minus_not
                              | dref=DEREF right=operation_unary_plus_minus_not
                              | operation_brackets;

operation_brackets: LEFT_ROUND_BRACE operation_logic_or RIGHT_ROUND_BRACE
                  | (function_use | variable_use | break_=BREAK | continue_=CONTINUE | constant ); // | const_array);

constant: int_=INT_ID | float_=FLOAT_ID | char_=CHAR_ID | str_=STR_ID;

//const_array: LEFT_CURLY_BRACE  constant (COMMA constant)* RIGHT_CURLY_BRACE;

//return_op: RETURN (return_val=(VAR_NAME|FLOAT_ID|CHAR_ID|INT_ID|ARRAY_VAR_NAME))?;
return_op: return_=RETURN (return_val=operation_logic_or)?;


// Reserved words
BREAK: 'break';
CONTINUE: 'continue';
RETURN: 'return';

// Special modifiers
IF: 'if';
ELSE: 'else';
WHILE: 'while';
FOR: 'for';

// Extra types
CONST: 'const';
VOID: 'void';

// Types
INT_TYPE: 'int';
FLOAT_TYPE: 'float';
CHAR_TYPE: 'char';

// Variables and indicators
VAR_NAME: [a-zA-Z_][a-zA-Z_0-9]*;
INT_ID: [0-9]+;
FLOAT_ID: [0-9]+[.]?[0-9]*;
CHAR_ID: '\'' . '\'';
STR_ID: '"' .*? '"';

// Indicators
SEMICOLON: ';';
COMMA: ',';
LEFT_ROUND_BRACE: '(';
RIGHT_ROUND_BRACE: ')';
LEFT_SQUARE_BRACE: '[';
RIGHT_SQUARE_BRACE: ']';
LEFT_CURLY_BRACE: '{';
RIGHT_CURLY_BRACE: '}';

// Special operations
ASSIGN: '=';
DEREF: '&';

// Logical operations
NOT: '!';
EQUAL: '==';
NOT_EQUAL: '!=';
LOGIC_OR: '||';
LOGIC_AND: '&&';
GREATER_THAN: '>';
LESS_THAN: '<';
LESS_THAN_OR_EQUAL: '<=';
GREATER_THAN_OR_EQUAL: '>=';

// Binary operations
MULT: '*';
PLUS: '+';
MINUS: '-';
DIV: '/';
MOD: '%';

// Unary operations
PLUS_PLUS: '++';
MIN_MIN: '--';

// Things to skip
WS: [ \t\r\n]+ -> skip;
MULTI_CMNT: '/*' .*? '*/' -> skip;
ONE_CMNT: '//' .*? '\n' -> skip;