grammar c;

start_rule: operation_sequence;

operation_sequence: (operation ';' |  if_statement | for_statement | while_statement | unnamed_scope)*;

unnamed_scope: '{' operation_sequence '}';

operation: (assignment | operation_logic_or | print_statement);

if_statement: 'if' '(' condition=operation_logic_or ')' '{' operation_sequence '}' (else_statement)?;

else_statement: 'else' '{' operation_sequence '}';

while_statement: 'while' '(' condition=operation_logic_or ')' '{' operation_sequence '}';

for_statement: 'for' '(' initialization=operation ';' condition=operation ';' step=operation ')' '{' operation_sequence '}';

print_statement: 'printf' '(' arg=(INT_ID | FLOAT_ID | CHAR_ID | VAR_NAME) ')';

assignment: lvalue ('=' operation_logic_or)?;

lvalue: ((CONST)? declaration=(INT_TYPE|FLOAT_TYPE|CHAR_TYPE) (MULT)?)? variable=VAR_NAME;

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

operation_brackets: '(' operation ')'
                  | (BREAK | CONTINUE | INT_ID | FLOAT_ID | CHAR_ID | VAR_NAME);

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
CONST: 'const';
BREAK: 'break';
CONTINUE: 'continue';
VAR_NAME: [a-zA-Z_][a-zA-Z_0-9]*;
INT_ID: [0-9]+;
FLOAT_ID: [0-9]+[.]?[0-9]*;
CHAR_ID: '\'' . '\'';
WS: [ \t\r\n]+ -> skip;
MULTI_CMNT: '/*' .*? '*/' -> skip;
ONE_CMNT: '//' .*? '\n' -> skip;