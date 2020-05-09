grammar llvm;

start_rule: (operation)* (declaration)*;

function: 'define' rettype=type_ '@' name=VAR_NAME '(' argument_list ')' scope;

argument_list: (argument)?(',' argument)*;

argument: type_;

use_arg_list: (use_argument)?(',' use_argument)*;

use_argument: normal_argument | string_argument;
string_argument: 'i8* getelementptr inbounds ([' c_count=INT_ID 'x i8], [' INT_ID 'x i8]* ' prtstr=variable ', i32 0, i32 0)';
normal_argument: type_ variable;

scope: '{' operation_sequence '}';

operation_sequence: operation+;

operation: return_ | assignment | store | function_call | function | label | branch;

label: name=VAR_NAME ':';

branch: conditional_branch | normal_branch;

conditional_branch: 'br' optype=type_ variable ', label' iftrue=variable ', label' iffalse=variable;
normal_branch: 'br' 'label' variable;

store: 'store' optype=type_ variable ',' type_'*' variable;

load: 'load' optype=type_ ',' type_'*' variable;

assignment: variable '=' rvalue;

rvalue: alocation | function_call | print_str | load | expression | extension | ptr_index;

extension: op=('fpext' | 'trunc' | 'sitofp' | 'sext' | 'zext' | 'fptosi' | 'fptoui' | 'fpext' | 'fptoui') type_from=type_ variable 'to' type_to=type_;

expression: binary | compare;
compare: float_compare | int_compare;
float_compare: 'fcmp' op=CMP_ID optype=type_ value  ',' value;
int_compare: 'icmp' op=CMP_ID optype=type_ value  ',' value;
binary: op=OP_ID optype=type_ value  ',' value;

alocation: ('alloca' | global_='global') optype=type_ ('undef')? ',' 'align' align_index=INT_ID;

value: variable | const_int | const_float;

const_int: INT_ID;

const_float: FLOAT_ID;

return_: 'ret' rettype=type_ (var=variable)?; // variable is optional in case of void

variable: ('%' | '@') var=(VAR_NAME | INT_ID); // %0 for arguments gives a lot of errors if i don't add int id

type_: (int_='i32'|float_='float'|char_='i8'|bool_='i1'|void_='void' | double_='double' | '...') (ptr='*')?; // ... for printf

function_call: 'call' rettype=type_ ('(' argument_list ')')? '@' fname=VAR_NAME '(' use_arg_list ')';
//print_function: 'call i32 (i8*, ...) @printf(' (',' use_arg_list)? ')';

print_str: 'private unnamed_addr constant [' c_count=INT_ID ' x i8] c' var=STR_ID ', align 1';

declaration: 'declare ' rettype=type_ '@' fname=VAR_NAME '(' argument_list ')'; // TODO: arglist and real name

ptr_index: 'getelementptr inbounds' array_type ',' array_type'*' variable ', i64 0, i64' index=INT_ID;
array_type: '[' max_count=INT_ID 'x' element_type=type_ ']';


OP_ID: ('add' | 'sub' | 'fadd' | 'fsub' | 'mul' | 'fmul' | 'fsub' | 'fdiv' | 'sdiv' | 'frem' | 'srem');
CMP_ID: ('sgt' | 'slt' | 'sle' | 'sge' | 'ne' | 'one' | 'olt' | 'slt' | 'ogt' | 'ole' | 'sle' | 'oge' | 'sge' | 'oeq' | 'eq');
INT_ID: [0-9]+;
FLOAT_ID: [0-9]+[.]?[0-9]*;
VAR_NAME: [a-zA-Z_0-9.]+;
STR_ID: '"' .*? '\\00"';
//CHAR_ID: '\'' . '\'';
//STR_ID: '"' .*? '"';
WS: [ \t\r\n]+ -> skip;
ONE_CMNT: ';' .*? '\n' -> skip;