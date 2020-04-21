grammar c;

start_rule: (include)? operation_sequence;

operation_sequence: (operation ';' | function |  if_statement | for_statement | while_statement | unnamed_scope)*;

include: '#include <stdio.h>';

function: function_declaration ';' | function_definition;

function_definition: (INT_TYPE|FLOAT_TYPE|CHAR_TYPE|VOID_TYPE) VAR_NAME '(' argument_list ')' '{' operation_sequence '}';

function_declaration: (INT_TYPE|FLOAT_TYPE|CHAR_TYPE|VOID_TYPE) VAR_NAME '(' argument_list ')';

function_use: VAR_NAME '(' use_argument_list ')';

use_argument_list: (operation_logic_or)?(',' operation_logic_or)*;

//use_argument: INT_ID|FLOAT_ID|CHAR_ID|VAR_NAME|STR_ID;

argument_list: (argument)?(',' argument)*;

argument: ((CONST)? declaration=(INT_TYPE|FLOAT_TYPE|CHAR_TYPE) (MULT)?) VAR_NAME;

unnamed_scope: '{' operation_sequence '}';

operation: (assignment | operation_logic_or | return_op);

if_statement: 'if' '(' condition=operation_logic_or ')' '{' operation_sequence '}' (else_statement)?;

else_statement: 'else' '{' operation_sequence '}';

while_statement: 'while' '(' condition=operation_logic_or ')' '{' operation_sequence '}';

for_statement: 'for' '(' initialization=operation ';' condition=operation ';' step=operation ')' '{' operation_sequence '}';

//print_statement: 'printf' '(' arg=(INT_ID | FLOAT_ID | CHAR_ID | VAR_NAME | ARRAY_VAR_NAME) ')';

assignment: declare | assign; // Must be a difference between them to prevent ambiguity x; (declaration or operation_logic_or?)

assign: lvalue '=' operation_logic_or;

lvalue: ((CONST)? declaration=(INT_TYPE|FLOAT_TYPE|CHAR_TYPE))? (MULT)? (variable=VAR_NAME ('[' array_index=INT_ID ']')?);

declare: ((CONST)? declaration=(INT_TYPE|FLOAT_TYPE|CHAR_TYPE)) (MULT)? (variable=VAR_NAME ('[' array_index=INT_ID ']')?);

operation_logic_or: left=operation_logic_or '||' right=operation_logic_and
                  | operation_logic_and;

operation_logic_and: left=operation_logic_and '&&' right=operation_compare_eq_neq
                   | operation_compare_eq_neq;

operation_compare_eq_neq: left=operation_compare_eq_neq ('=='|'!=') right=operation_compare_leq_geq_l_g
                        | operation_compare_leq_geq_l_g;

operation_compare_leq_geq_l_g: left=operation_compare_leq_geq_l_g ('>'|'<'|'<='|'>=') right=operation_plus_minus
                             | operation_plus_minus;

operation_plus_minus: left=operation_plus_minus ('+'|'-') right=operation_mult_div
                    | operation_mult_div;

operation_mult_div: left=operation_mult_div ('*'|'/'|'%') right=operation_unary_plus_minus_not
                  | operation_unary_plus_minus_not;

operation_unary_plus_minus_not: '++' right=operation_unary_plus_minus_not
                              | '--' right=operation_unary_plus_minus_not
                              | '+' right=operation_unary_plus_minus_not
                              | '-' right=operation_unary_plus_minus_not
                              | '!' right=operation_unary_plus_minus_not
                              | '*' right=operation_unary_plus_minus_not
                              | '&' right=operation_unary_plus_minus_not
                              | operation_brackets;

operation_brackets: '(' operation_logic_or ')'
                  | (function_use | array_var_name | BREAK | CONTINUE | INT_ID | FLOAT_ID | CHAR_ID | VAR_NAME | const_array | STR_ID);

array_var_name: var=VAR_NAME '[' nr=INT_ID ']';

const_array: '{'  const_array_element (',' const_array_element)* '}';
const_array_element: (VAR_NAME|INT_ID|FLOAT_ID|CHAR_ID);

//return_op: RETURN (return_val=(VAR_NAME|FLOAT_ID|CHAR_ID|INT_ID|ARRAY_VAR_NAME))?;
return_op: RETURN (return_val=operation_logic_or)?;

DOUBLE_PLUS: '++';
DOUBLE_MIN: '--';
PLUS: '+';
MIN: '-';
NOT: '!';
NEQ: '!=';
EQ: '==';
GEQ: '>=';
LEQ: '<=';
LT: '<';
GT: '>';
DIV: '/';
MOD: '%';
LBR: '(';
RBR: ')';
MULT: '*';
LAND: '&&';
LOR: '||';
SEMI: ';';
REF: '&';
ASSIGN: '=';
INT_TYPE: 'int';
FLOAT_TYPE: 'float';
CHAR_TYPE: 'char';
VOID_TYPE: 'void';
//ARRAY_ID: '{' (VAR_NAME|INT_ID|FLOAT_ID|CHAR_ID) (','(VAR_NAME|INT_ID|FLOAT_ID|CHAR_ID))* '}';
CONST: 'const';
BREAK: 'break';
CONTINUE: 'continue';
RETURN: 'return';
RESERVED_WORD: ('if' | 'else' | 'while' | 'for'); //https://stackoverflow.com/questions/9726620/how-can-i-differentiate-between-reserved-words-and-variables-using-antlr
//ARRAY_VAR_NAME: [a-zA-Z_][a-zA-Z_0-9]* '[' (INT_ID)? ']';
VAR_NAME: [a-zA-Z_][a-zA-Z_0-9]*;
INT_ID: [0-9]+;
FLOAT_ID: [0-9]+[.]?[0-9]*;
CHAR_ID: '\'' . '\'';
STR_ID: '"' .*? '"';
WS: [ \t\r\n]+ -> skip;
MULTI_CMNT: '/*' .*? '*/' -> skip;
ONE_CMNT: '//' .*? '\n' -> skip;