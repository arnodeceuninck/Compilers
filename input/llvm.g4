grammar llvm;

start_rule: (operation)* (declaration)*;

function: 'define' rettype=type_ '@' name=VAR_NAME '()' scope;

scope: '{' operation_sequence '}';

operation_sequence: operation+;

operation: return_ | assignment | store | function_call | function;

store: 'store' optype=type_ variable ',' type_'*' variable;

assignment: variable '=' rvalue;

rvalue: alocation | addition | function_call | print_str;

alocation: 'alloca' optype=type_ ',' 'align' align_index=INT_ID;

addition: 'add' optype=type_ value  ',' value;

value: variable | const_int;

const_int: INT_ID;

return_: 'ret' type_ variable;

variable: ('%' | '@') var=VAR_NAME;

type_: (int_='i32'|float_='float'|char_='i8'|bool_='i1');

function_call: print_function;
print_function: 'call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([2 x i8], [2 x i8]* ' prtstr=variable ', i32 0, i32 0))';

print_str: 'private unnamed_addr constant [2 x i8] c"' var=VAR_NAME '\\00", align 1';

declaration: 'declare i32 @printf(i8*, ...)';


VAR_NAME: [a-zA-Z.][a-zA-Z_0-9.]*;
INT_ID: [0-9]+;
//FLOAT_ID: [0-9]+[.]?[0-9]*;
//CHAR_ID: '\'' . '\'';
//STR_ID: '"' .*? '"';
WS: [ \t\r\n]+ -> skip;
ONE_CMNT: ';' .*? '\n' -> skip;