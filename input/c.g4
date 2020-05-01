grammar c;

start_rule: (include)? operation_sequence;

include: '#include <stdio.h>';

operation_sequence: (operation ';' | function |  if_statement | for_statement | while_statement | scope)*;

scope: '{' operation_sequence '}';

function: function_declaration ';' | function_definition;

function_definition: function_declaration scope;

function_declaration: type_ var=VAR_NAME '(' argument_list ')';

type_: (int_='int'|float_='float'|char_='char'|void_='void');

variable_declaration: ((const_='const')? declaration=type_) variable_use;  // TODO: int f[0](){} shouldn't be allowed.

variable_use: (pointer)* var=VAR_NAME (array=array_index)?;

array_index: '[' index=operation_logic_or ']';

pointer: '*';

function_use: var=VAR_NAME '(' use_argument_list ')';

use_argument_list: (operation_logic_or)?(',' operation_logic_or)*;

argument_list: (variable_declaration)?(',' variable_declaration)*;

operation: (assignment | operation_logic_or | return_op);

if_statement: 'if' '(' condition=operation_logic_or ')' scope (else_statement)?;

else_statement: 'else' scope;

while_statement: 'while' '(' condition=operation_logic_or ')' scope;

for_statement: 'for' '(' (assignment | operation_logic_or) ';' (assignment | operation_logic_or) ';' (assignment |operation_logic_or) ')' scope;

assignment: variable_declaration | assign; // Must be a difference between them to prevent ambiguity x; (declaration or operation_logic_or?)

assign: lvalue '=' operation_logic_or;

lvalue: variable_declaration | variable_use;

operation_logic_or: left=operation_logic_or lor='||' right=operation_logic_and
                  | operation_logic_and;

operation_logic_and: left=operation_logic_and land='&&' right=operation_compare_eq_neq
                   | operation_compare_eq_neq;

operation_compare_eq_neq: left=operation_compare_eq_neq (eq='=='|neq='!=') right=operation_compare_leq_geq_l_g
                        | operation_compare_leq_geq_l_g;

operation_compare_leq_geq_l_g: left=operation_compare_leq_geq_l_g (gt='>'|lt='<'|leq='<='|geq='>=') right=operation_plus_minus
                             | operation_plus_minus;

operation_plus_minus: left=operation_plus_minus (plus='+'|minus='-') right=operation_mult_div
                    | operation_mult_div;

operation_mult_div: left=operation_mult_div (mult='*'|div='/'|mod='%') right=operation_unary_plus_minus_not
                  | operation_unary_plus_minus_not;

operation_unary_plus_minus_not: pp='++' right=operation_unary_plus_minus_not
                              | mm='--' right=operation_unary_plus_minus_not
                              | plus='+' right=operation_unary_plus_minus_not
                              | minus='-' right=operation_unary_plus_minus_not
                              | not_='!' right=operation_unary_plus_minus_not
                              | rref='*' right=operation_unary_plus_minus_not
                              | dref='&' right=operation_unary_plus_minus_not
                              | operation_brackets;

operation_brackets: '(' operation_logic_or ')'
                  | (function_use | variable_use | break_='break' | continue_='continue' | constant ); // | const_array);

constant: int_=INT_ID | float_=FLOAT_ID | char_=CHAR_ID | str_=STR_ID;

//const_array: '{'  constant (',' constant)* '}';

//return_op: RETURN (return_val=(VAR_NAME|FLOAT_ID|CHAR_ID|INT_ID|ARRAY_VAR_NAME))?;
return_op: return_='return' (return_val=operation_logic_or)?;


RESERVED_WORD: ('if' | 'else' | 'while' | 'for' | 'const' | 'break' | 'continue' | 'return' | 'int' | 'float' | 'char' | 'void'); //https://stackoverflow.com/questions/9726620/how-can-i-differentiate-between-reserved-words-and-variables-using-antlr
VAR_NAME: [a-zA-Z_][a-zA-Z_0-9]*;
INT_ID: [0-9]+;
FLOAT_ID: [0-9]+[.]?[0-9]*;
CHAR_ID: '\'' . '\'';
STR_ID: '"' .*? '"';
WS: [ \t\r\n]+ -> skip;
MULTI_CMNT: '/*' .*? '*/' -> skip;
ONE_CMNT: '//' .*? '\n' -> skip;