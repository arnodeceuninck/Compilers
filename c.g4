grammar c;
start_rule: operation_block;

operation_block: operation ';'
                | operation ';' operation_block;

operation: operation_compare_eq_neq;

operation_logic_or: operation_logic_or '||' operation_logic_and
                    | operation_logic_and;

operation_logic_and: operation_logic_and '&&' operation_compare_eq_neq
                    | operation_compare_eq_neq;

operation_compare_eq_neq: operation_compare_eq_neq '==' operation_compare_leq_geq_l_g
                    | operation_compare_eq_neq '!=' operation_compare_leq_geq_l_g
                    | operation_compare_leq_geq_l_g;

operation_compare_leq_geq_l_g: operation_compare_leq_geq_l_g '>' operation_plus_minus
                        | operation_compare_leq_geq_l_g '<' operation_plus_minus
                        | operation_compare_leq_geq_l_g '<=' operation_plus_minus
                        | operation_compare_leq_geq_l_g '>=' operation_plus_minus
                        | operation_plus_minus;

operation_plus_minus: operation_plus_minus '+' operation_mult_div
                  | operation_plus_minus '-' operation_mult_div
                  | operation_mult_div;

operation_mult_div: operation_mult_div '*' operation_unary_plus_minus_not
                | operation_mult_div '/' operation_unary_plus_minus_not
                | operation_mult_div '%' operation_unary_plus_minus_not
                | operation_unary_plus_minus_not;

operation_unary_plus_minus_not: '+' operation_brackets
                          | '-' operation_brackets
                          | '!' operation_brackets
                          | operation_brackets;

operation_brackets: '(' operation ')'
                | ID;

ID: [0-9]+;
WS: [ \t\r\n]+ -> skip;