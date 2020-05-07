grammar llvm;

start_rule: (operation)* (declaration)*;

function: 'define' rettype=type_ '@' name=VAR_NAME '(' argument_list ')' scope;

argument_list: (argument)?(',' argument)*;

argument: type_;

use_arg_list: (use_argument)?(',' use_argument)*;

use_argument: type_ variable;

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

variable: ('%' | '@') var=(VAR_NAME | INT_ID); // %0 for arguments gives a lot of errors if i don't add int id

type_: (int_='i32'|float_='float'|char_='i8'|bool_='i1'|void_='void' | '...') (ptr='*')?; // ... for printf

function_call: print_function | own_function;
own_function: 'call' rettype=type_ '@' fname=VAR_NAME '(' use_arg_list ')';
print_function: 'call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([' c_count=INT_ID 'x i8], [' INT_ID 'x i8]* ' prtstr=variable ', i32 0, i32 0))';

print_str: 'private unnamed_addr constant [' c_count=INT_ID ' x i8] c' var=STR_ID ', align 1';

declaration: 'declare ' rettype=type_ '@' fname=VAR_NAME '(' argument_list ')'; // TODO: arglist and real name


OP_ID: ('add' | 'sub' | 'fadd' | 'fsub');
INT_ID: [0-9]+;
FLOAT_ID: [0-9]+[.]?[0-9]*;
VAR_NAME: [a-zA-Z_0-9.]+;
STR_ID: '"' .*? '\\00"';
//CHAR_ID: '\'' . '\'';
//STR_ID: '"' .*? '"';
WS: [ \t\r\n]+ -> skip;
ONE_CMNT: ';' .*? '\n' -> skip;