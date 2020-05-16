grammar llvm;

start_rule: (operation)* (declaration)*;

function: 'define' rettype=type_ '@' name=VAR_NAME '(' argument_list ')' scope;

argument_list: (argument)?(',' argument)*;

argument: type_;

use_arg_list: (use_argument)?(',' use_argument)*;

use_argument: typed_variable | string_argument;
typed_variable: type_ value;
string_argument: 'i8* getelementptr inbounds ([' c_count=INT_ID ' x i8], [' INT_ID ' x i8]* ' prtstr=variable ', i32 0, i32 0)';

scope: '{' operation_sequence '}';

operation_sequence: operation+;

operation: return_ | assignment | store | function_call | function | label | branch;

label: name=VAR_NAME ':';

branch: conditional_branch | normal_branch;

conditional_branch: 'br' typed_variable ', label' iftrue=variable ', label' iffalse=variable;
normal_branch: 'br' 'label' variable;

store: 'store' typed_variable ',' typed_variable (', align' align=INT_ID)?; // same todo as with load

load: 'load' optype=type_ ',' typed_variable (', align' align=INT_ID)?; // TODO: is align required in tree? probably it is for arrays

assignment: variable '=' rvalue;

rvalue: alocation | function_call | print_str | load | expression | extension | ptr_index;

extension: op=('fpext' | 'trunc' | 'sitofp' | 'sext' | 'zext' | 'fptosi' | 'fptoui' | 'fpext' | 'fptoui' | 'uitofp') variable_from=typed_variable 'to' type_to=type_;

expression: binary | compare;
compare: float_compare | int_compare;
float_compare: 'fcmp' op=CMP_ID typed_variable  ',' value;
int_compare: 'icmp' op=CMP_ID optype=typed_variable  ',' value;
binary: op=OP_ID optype=typed_variable  ',' value;

alocation: ('alloca' | global_='global') optype=type_ ('undef')? ', align' align_index=INT_ID;

value: variable | const_int | const_float;

const_int: INT_ID;

const_float: FLOAT_ID;

return_: 'ret' rettype=type_ (var=variable)?; // variable is optional in case of void

variable: ('%' | '@') var=(VAR_NAME | INT_ID); // %0 for arguments gives a lot of errors if i don't add int id

type_: normal_type | array=array_type;
normal_type: (int_='i32'|float_='float'|char_='i8'|bool_='i1'|void_='void' | double_='double' | double='i64' | '...') (ptr='*')*; // ... for printf
array_type: '[' max_count=INT_ID ' x ' element_type=normal_type ']';

function_call: 'call' rettype=type_ ('(' argument_list ')')? '@' fname=VAR_NAME '(' use_arg_list ')';
//print_function: 'call i32 (i8*, ...) @printf(' (',' use_arg_list)? ')';

print_str: 'private unnamed_addr constant [' c_count=INT_ID ' x i8] c' var=STR_ID ', align' align_id=INT_ID;

declaration: 'declare ' rettype=type_ '@' fname=VAR_NAME '(' argument_list ')'; // TODO: arglist and real name

ptr_index: 'getelementptr inbounds' a_type=array_type ',' typed_variable ', i64 0, i64' index=value;

OP_ID: ('add' | 'sub' | 'fadd' | 'fsub' | 'mul' | 'fmul' | 'fsub' | 'fdiv' | 'sdiv' | 'frem' | 'srem');
CMP_ID: ('sgt' | 'slt' | 'sle' | 'sge' | 'ne' | 'one' | 'olt' | 'ogt' | 'ole' | 'sle' | 'oge' | 'sge' | 'oeq' | 'eq');
INT_ID: [0-9]+;
FLOAT_ID: [0-9]+[.]?[0-9]*;
VAR_NAME: [a-zA-Z_0-9.]+;
STR_ID: '"' .*? '\\00"';
//CHAR_ID: '\'' . '\'';
//STR_ID: '"' .*? '"';
WS: [ \t\r\n]+ -> skip;
ONE_CMNT: ';' .*? '\n' -> skip;