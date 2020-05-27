grammar llvm;

start_rule: (operation)* (declaration)*;

function: DEFINE rettype=type_ AT name=VAR_NAME OPEN_BRACK argument_list CLOSE_BRACK scope;

argument_list: (argument)?(COMMA argument)*;

argument: type_;

use_arg_list: (use_argument)?(COMMA use_argument)*;

use_argument: typed_variable; // | string_argument;
typed_variable: type_ value;
//string_argument: 'i8* getelementptr inbounds ([' c_count=INT_ID ' x i8], [' INT_ID ' x i8]* ' prtstr=variable ', i32 0, i32 0)';

scope: OPEN_CURLY operation_sequence CLOSE_CURLY;

operation_sequence: operation+;

operation: return_ | assignment | store | function_call | function | label | branch;

label: name=VAR_NAME COLON;

branch: conditional_branch | normal_branch;

conditional_branch: BRANCH typed_variable COMMA LABEL iftrue=variable COMMA LABEL iffalse=variable;
normal_branch: BRANCH LABEL variable;

store: STORE typed_variable COMMA typed_variable (COMMA ALIGN align=INT_ID)?; // same todo as with load

load: LOAD optype=type_ COMMA typed_variable (COMMA ALIGN align=INT_ID)?; // TODO: is align required in tree? probably it is for arrays

assignment: variable EQ rvalue;

rvalue: alocation | function_call | print_str | load | expression | extension | ptr_index;

extension: op=EXT_OP variable_from=typed_variable TO type_to=type_;

expression: binary | compare;
compare: float_compare | int_compare;
float_compare: FCMP op=CMP_ID typed_variable  COMMA value;
int_compare: ICMP op=CMP_ID optype=typed_variable  COMMA value;
binary: op=OP_ID optype=typed_variable  COMMA value;

alocation: (ALLOCA | global_=GLOBAL) optype=type_ (UNDEF)? COMMA ALIGN align_index=INT_ID;

value: variable | const_int | const_float | ptr_index;

const_int: INT_ID;

const_float: FLOAT_ID;

return_: RETURN rettype=type_ (var=variable)?; // variable is optional in case of void

variable: (PERCENT | AT) var=(VAR_NAME | INT_ID); // %0 for arguments gives a lot of errors if i don't add int id

type_: normal_type | array=array_type;
normal_type: (int_=INT|float_=FLOAT|char_=CHAR|bool_=BOOL|void_=VOID | double_=DOUBLE | double=BIG_INT | ELLIPS) (ptr=PTR)*; // ... for printf
array_type: OPEN_SQUARE max_count=INT_ID ARRAY_MULT element_type=normal_type CLOSE_SQUARE (ptr=PTR)*;

function_call: CALL rettype=type_ (OPEN_BRACK argument_list CLOSE_BRACK)? AT fname=VAR_NAME OPEN_BRACK use_arg_list CLOSE_BRACK;
//print_function: 'call i32 (i8*, ...) @printf(' (COMMA use_arg_list)? CLOSE_BRACK;

print_str: PRNTSTR_HEAD c_count=INT_ID PRNTSTR_TAIL var=STR_ID COMMA ALIGN align_id=INT_ID;

declaration: DECLARE rettype=type_ AT fname=VAR_NAME OPEN_BRACK argument_list CLOSE_BRACK; // TODO: arglist and real name

ptr_index: GET_PTR OPEN_BRACK? a_type=array_type COMMA typed_variable COMMA (BIG_INT | INT) INT_ID COMMA (BIG_INT | INT) index=value CLOSE_BRACK?; // INT_ID is always zero in our generated LLVM code

OPEN_CURLY: '{';
CLOSE_CURLY: '}';
OPEN_BRACK: '(';
CLOSE_BRACK: ')';
OPEN_SQUARE: '[';
CLOSE_SQUARE: ']';

DECLARE: 'declare';
DEFINE: 'define';
CALL: 'call';
RETURN: 'ret';

AT: '@';
COMMA: ',';
COLON: ':';
EQ: '=';
PERCENT: '%';

BRANCH: 'br';
LABEL: 'label';

ALIGN: 'align';
STORE: 'store';
LOAD: 'load';

TO: 'to';

ALLOCA: 'alloca';
GLOBAL: 'global';
UNDEF: 'undef';

GET_PTR: 'getelementptr inbounds';

INT: 'i32';
BIG_INT: 'i64';
FLOAT: 'float';
DOUBLE: 'double';
BOOL: 'i1';
CHAR: 'i8';
VOID: 'void';
ELLIPS: '...';

PTR: '*';

PRNTSTR_HEAD: 'private unnamed_addr constant [';
PRNTSTR_TAIL: ' x i8] c';

ARRAY_MULT: ' x ';

FCMP: 'fcmp';
ICMP: 'icmp';

OP_ID: ('add' | 'sub' | 'fadd' | 'fsub' | 'mul' | 'fmul' | 'fsub' | 'fdiv' | 'sdiv' | 'frem' | 'srem');
CMP_ID: ('sgt' | 'slt' | 'sle' | 'sge' | 'ne' | 'one' | 'olt' | 'ogt' | 'ole' | 'sle' | 'oge' | 'sge' | 'oeq' | 'eq');
EXT_OP: ('fpext' | 'trunc' | 'sitofp' | 'sext' | 'zext' | 'fptosi' | 'fptoui' | 'fpext' | 'fptoui' | 'uitofp');

INT_ID: [0-9]+;
FLOAT_ID: [0-9]+[.]?[0-9]*;
VAR_NAME: [a-zA-Z_0-9.]+;
STR_ID: '"' .*? '\\00"';
//CHAR_ID: '\'' . '\'';
//STR_ID: '"' .*? '"';
WS: [ \t\r\n]+ -> skip;
ONE_CMNT: ';' .*? '\n' -> skip;