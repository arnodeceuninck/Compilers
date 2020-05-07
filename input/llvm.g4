grammar llvm;

start_rule: (operation)* (declaration)*;

function: 'define' rettype=type_ '@' name=VAR_NAME '()' scope;

scope: '{' operation_sequence '}';

operation_sequence: operation+;

operation: return_ | assignment | store | function_call | function;

store: 'store' optype=type_ variable ',' type_'*' variable;

load: 'load' optype=type_ ',' type_'*' variable;

assignment: variable '=' rvalue;

rvalue: alocation | function_call | print_str | load | expression;

expression: binary;
binary: op=OP_ID optype=type_ value  ',' value;

alocation: 'alloca' optype=type_ ',' 'align' align_index=INT_ID;

value: variable | const_int | const_float;

const_int: INT_ID;

const_float: FLOAT_ID;

return_: 'ret' rettype=type_ variable;

variable: ('%' | '@') var=VAR_NAME;

type_: (int_='i32'|float_='float'|char_='i8'|bool_='i1');

function_call: print_function;
print_function: 'call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([2 x i8], [2 x i8]* ' prtstr=variable ', i32 0, i32 0))';

print_str: 'private unnamed_addr constant [2 x i8] c"' var=VAR_NAME '\\00", align 1';

declaration: 'declare ' rettype=type_ '@' fname='printf' '(i8*, ...)';


VAR_NAME: [a-zA-Z.][a-zA-Z_0-9.]*;
INT_ID: [0-9]+;
FLOAT_ID: [0-9]+[.]?[0-9]*;
OP_ID: ('add' | 'sub' | 'fadd' | 'fsub')
//CHAR_ID: '\'' . '\'';
//STR_ID: '"' .*? '"';
WS: [ \t\r\n]+ -> skip;
ONE_CMNT: ';' .*? '\n' -> skip;