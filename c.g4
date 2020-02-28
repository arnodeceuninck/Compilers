grammar c;
startRule: operationCompareEq ';';
operationCompareEq: operationCompareEq '==' operationCompareLeqGeqLG
                    | operationCompareLeqGeqLG;

operationCompareLeqGeqLG: operationCompareLeqGeqLG '>' operationPlusMinus
                        | operationCompareLeqGeqLG '<' operationPlusMinus
                        | operationCompareLeqGeqLG '<=' operationPlusMinus
                        | operationCompareLeqGeqLG '>=' operationPlusMinus
                        | operationPlusMinus;

operationPlusMinus: operationPlusMinus '+' operationMultDiv
                  | operationPlusMinus '-' operationMultDiv
                  | operationMultDiv;

operationMultDiv: ID '*' ID
                | ID '/' ID
                | ID '%' ID
                | ID;

ID: [0-9]+;
WS: [ \t\r\n]+ -> skip;