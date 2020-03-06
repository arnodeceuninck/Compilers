grammar c;
start_rule: operation_block;

operation_block: operation ';'
                | operation ';' operation_block;

operation: operation_logic_or;

operation_logic_or: left=operation_logic_or '||' right=operation_logic_and
                    | operation_logic_and;

operation_logic_and: left=operation_logic_and '&&' right=operation_compare_eq_neq
                    | operation_compare_eq_neq;

operation_compare_eq_neq: left=operation_compare_eq_neq '==' right=operation_compare_leq_geq_l_g
                    | left=operation_compare_eq_neq '!=' right=operation_compare_leq_geq_l_g
                    | operation_compare_leq_geq_l_g;

operation_compare_leq_geq_l_g: left=operation_compare_leq_geq_l_g '>' right=operation_plus_minus
                        |left= operation_compare_leq_geq_l_g '<' right=operation_plus_minus
                        | left=operation_compare_leq_geq_l_g '<=' right=operation_plus_minus
                        | left=operation_compare_leq_geq_l_g '>=' right=operation_plus_minus
                        | operation_plus_minus;

operation_plus_minus: left=operation_plus_minus '+' right=operation_mult_div
                  | left=operation_plus_minus '-' right=operation_mult_div
                  | operation_mult_div;

operation_mult_div: left=operation_mult_div '*' right=operation_unary_plus_minus_not
                | left=operation_mult_div '/' right=operation_unary_plus_minus_not
                | left=operation_mult_div '%' right=operation_unary_plus_minus_not
                | operation_unary_plus_minus_not;

operation_unary_plus_minus_not: '+' operation_brackets
                          | '-' operation_brackets
                          | '!' operation_brackets
                          | operation_brackets;

operation_brackets: '(' operation ')'
                | ID;

ID: [0-9]+;
WS: [ \t\r\n]+ -> skip;