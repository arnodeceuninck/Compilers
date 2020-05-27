# Compilers
## Auteurs
Arno Deceuninck & Basil Rommens
## Quickstart
```run.sh``` for running ```main.py``` with ```y.c```

```test.sh``` for running unittests
## Opgave
### 1. Expressions
#### Mandatory
- [x] Binary operations +, -, * and /
- [x] Binary operations >, < and ==
- [x] Unary operators + and -
- [x] Brackets to overwrite the order of operations
- [x] AST
#### Optional
- [x] Binary operator %
- [x] Comparison operators >=, <=, and !=
- [x] Logical operators &&, ||, and !


### 2. Variables
#### Mandatory
- [x] Types (char, float, int and pointer)
- [x] Reserved words (const)
- [x] Variables
- [x] AST

#### Optional
- [ ] Identifier operations (++ and --)
- [ ] Conversions


### 3. LLVM
#### Mandatory
- [x] Comments (single line and multiline)
- [x] Printf
- [x] LLVM generation (niet mogelijk om pointers te gebruiken)

#### Optional
- [ ] Retaining comments in compilation process
- [x] Comment after every instruction that contains the statement from the input code


### 4. Loops and conditionals
#### Mandatory
- [x] Reserved words: If
- [x] Reserved words: Else
- [x] Reserved words: While
- [x] Reserved words: For
- [x] Reserved words: Break
- [x] Reserved words: Continue
- [x] Scopes: unnamed scopes
- [x] Scopes: Loops
- [x] Scopes: Conditionals

#### Optional
- [ ] Reserved words: Switch
- [ ] Reserved words: Case
- [ ] Reserved words: Default


### 5. Functions
#### Mandatory
- [x] Reserved words: return
- [x] Reserved words: void
- [x] Scopes: function
- [x] Local and global variables
- [x] Functions
- [x] Do not generate code after return statement
- [x] Do not generate code after break or continue

#### Optional
- [ ] Do not generate code for variables that are not used
- [ ] Do not generate code for conditionals that are always false
- [ ] Check if all functions end with return

### 6. Arrays
#### Mandatory
- [x] Arrays
- [x] Import: printf(char *format, ...)
- [x] Import: intf(const char *format, ...)

#### Optional
- [ ] Arrays: Multi-dimensional
- [ ] Arrays: assignments of complete arrays or array rows in case of multi-dimensional arrays
- [ ] Arrays: Dynamic arrays

## LLVM Generatie
Om llvm leesbaar te houden voor ons en het eenvoudig te houden in presentatie, maken we gebruik van verschillende middelen.
### Variabelen
Voor de llvm generatie van variabelen zorgen we er voor dat er geen overlap gebeurt tussen de variabelen op de volgende manier.
Het **eerste** wat we doen is **globale variabelen** hun gewone naam laten houden _(<var_name>)_. **Andere variabelen** worden anders behandeld.
Indien we deze tegenkomen nemen we de variabele naam en plakken we achter de variabele een . en dan nog de id van de node waar ze
in zitten _(<var_name> + . + <node_id>)_. Het punt dient er voor dat variabelen niet met een getal kunnen overeenkomen als we dit op een of andere manier proberen te bereiken.
Het punt kan je niet in c gebruiken bij een variabele naam. Dan hebben we de **automatisch gegenereerde variabelen** die beginnen altijd
met een punt en worden gevolgd door een letter, dit kan een _v_ of een _t_ zijn. _v_ wijst op een variabele die wordt later meestal gebruikt, terwijl t wijst 
op een tijdelijke variabele, deze is altijd anders wanneer men die genereerd van een node. Na deze letter volgt een unieke id
bij een _t_ is die bij elke generatie anders, maar bij een _v_ is die gelijk aan de id van de node zo blijft deze variabele herbruikbaard _(. + t|v + <id>)_.
Tot slot hebben we nog de strings die er gebruikt worden in `printf` en `scanf`. Deze zijn van de volgende structuur (. + str + . + <node_id>).
### Comentaren
We zorgen er ook voor dat er bij de llvm generatie commentaren bij komen, dit zorgt er grotendeels voor dat we de snel kunnen terugvinden
waar we eventueel een fout in hebben gemaakt. Ook worden code blokken aangeduid, let wel op dat dit niet enorm betrouwbaar is.
Het enigste waar we in commentaren generatie in verschillen is dat deze voor de llvm statements gebeurd.

## MIPS generatie
Om mips te genereren vertrekken we vanuit llvm. Zo kunnen we veel dubbel werk vermijden, zoals het bepalen van scopes,
variabelen toekennen enz.
### Variabelen
We slaan al de variabelen op in de stack. We zoeken eerst al de gebruikte variablen in de llvm code en bepalen dan hoe groot
de stack moet zijn. Omdat er geen enkele variabele overlap heeft ook niet met functies, kunnen we de stackpointer relatief klein houden.
Zo moeten we geen rekening houden met de variabelen die reeds gebruikt zijn, met de doorgegeven argumenten is er een speciale operatie nodig, net als al de variabelen
in de functie, die moeten ook opgeslagen worden. Dit gebeurd met de stackpointer

## Opmerkingen
Indien er een bewerking wordt gedaan op 2 integer getallen, wordt de uitkomst afgerond en omgezet naar een int

## Node klasse
### Structuur
![alt text](doc/NodeClass.png)

### Histogram
- ![#ffd885](https://placehold.it/15/ffd885/000000?text=+) Constanten
- ![#87f5ff](https://placehold.it/15/87f5ff/000000?text=+) Operatoren
- ![#af93ff](https://placehold.it/15/af93ff/000000?text=+) Variabelen
- ![#ff6486](https://placehold.it/15/ff6486/000000?text=+) Gereserveeerde types
- ![#adff77](https://placehold.it/15/adff77/000000?text=+) Functies en argumentenlijst
- ![#38A038](https://placehold.it/15/38A038/000000?text=+) Commentaren
- ![#000000](https://placehold.it/15/000000/000000?text=+) Include
- ![#9f9f9f](https://placehold.it/15/9f9f9f/000000?text=+) Default Nodes

## Escape Sequences
Omdat het ridicuul zou zijn om elke mogelijke escape sequence van c te implementeren, hebben we er slechts eensubset van geimplementeerd. Deze subset is in de afbeelding hieronder afgebeeld.
![alt text](doc/escape_sequences.png)

## Testen
In de tests folder vind je een bestand ```test.py```. Als je dit runt (eventueel ```test.sh```, runnen er ineens een paar testen. De uitleg waarvoor
welke test specifiek dient kan je terugvinden in het c bestand van de test zelf (in de folder ```tests/input```). Om specifiek te weten waarop de testen werken, kan je een kijkje nemen in het ```tests/test.py```. 

## Benchmark Result (102/111)
The Benchmark tests have been changed from the given ones, because we don't support for example `i++`, so had to change this everywhere to `i = i + 1`.
### CorrectCode (28/32)
- [x] binaryOperations1.c
- [x] binaryOperations2.c
- [x] breakAndContinue.c
- [ ] comparisons1.c
- [ ] comparisons2.c
- [x] dereferenceAssignment.c
- [x] fibonacciRecursive.c
- [ ] floatToIntConversion.c
- [x] for.c
- [x] forwardDeclaration.c
- [x] if.c
- [x] ifElse.c
- [ ] intToFloatConversion.c
- [x] modulo.c
- [x] pointerArgument.c
- [x] prime.c
- [x] printf1.c
- [x] printf2.c
- [x] printf3.c
- [x] scanf1.c
- [ ] scanf2.c (passes because manual input required)
- [x] scoping.c
- [x] unaryOperations.c
- [x] variables1.c
- [x] variables2.c
- [x] variables3.c
- [x] variables4.c
- [x] variables5.c
- [x] variables6.c
- [x] variables7.c
- [x] variables8.c
- [x] while.c

### SemanticErrors (46/47)
- [x] arrayAccessTypeMismatch2.c
- [x] arrayAccessTypeMismatch.c
- [x] arrayCompareError.c
- [x] arraySizeTypeMismatch.c
- [x] declarationDeclarationMismatch1.c
- [x] declarationDeclarationMismatch2.c
- [x] declarationDeclarationMismatch3.c
- [x] declarationDefinitionMismatch1.c
- [x] declarationDefinitionMismatch2.c
- [x] declarationDefinitionMismatch3.c
- [x] definitionInLocalScope.c
- [x] dereferenceTypeMismatch1.c
- [x] dereferenceTypeMismatch2.c
- [x] functionCallargumentMismatch1.c
- [x] functionCallargumentMismatch2.c
- [x] functionCallargumentMismatch3.c
- [x] functionCallargumentMismatch4.c
- [x] functionRedefinition1.c
- [x] functionRedefinition2.c
- [x] functionRedefinition3.c
- [x] incompatibleTypes1.c
- [x] incompatibleTypes2.c
- [x] incompatibleTypes3.c
- [x] incompatibleTypes4.c
- [x] incompatibleTypes5.c
- [x] incompatibleTypes6.c
- [x] incompatibleTypes7.c
- [x] invalidIncludeError.c
- [x] invalidLoopControlStatement.c
- [ ] invalidUnaryOperation.c
- [x] mainNotFound.c
- [x] parameterRedefinition1.c
- [x] parameterRedefinition2.c
- [x] parameterRedefinition3.c
- [x] pointerOperationError.c
- [x] returnOutsideFunction.c
- [x] returnTypeMismatch.c
- [x] undeclaredFunction.c
- [x] undeclaredVariable1.c
- [x] undeclaredVariable2.c
- [x] undeclaredVariable3.c
- [x] variableRedefinition1.c
- [x] variableRedefinition2.c
- [x] variableRedefinition3.c
- [x] variableRedefinition4.c
- [x] variableRedefinition5.c
- [x] variableRedefinition6.c

###MIPS tests (28/32)
- [x] binaryOperations1.c
- [x] binaryOperations2.c
- [x] breakAndContinue.c
- [ ] comparisons1.c
- [ ] comparisons2.c
- [x] dereferenceAssignment.c
- [x] fibonacciRecursive.c
- [ ] floatToIntConversion.c
- [x] for.c
- [x] forwardDeclaration.c
- [x] if.c
- [x] ifElse.c
- [ ] intToFloatConversion.c
- [x] modulo.c
- [x] pointerArgument.c
- [x] prime.c
- [x] printf1.c
- [x] printf2.c
- [x] printf3.c
- [x] scanf1.c
- [ ] scanf2.c (passes because manual input required)
- [x] scoping.c
- [x] unaryOperations.c
- [x] variables1.c
- [x] variables2.c
- [x] variables3.c
- [x] variables4.c
- [x] variables5.c
- [x] variables6.c
- [x] variables7.c
- [x] variables8.c
- [x] while.c

## Explenation
### Part 1 (Intermiate Project Evaluation)
#### Grammar structure (Arno)
- Start with optional include and operation sequence
- operation sequence can be an operation, function, conditional statement or unnamed scope
- operation can be an assignment, return operation or arithmetic operation

#### AST (Basil)
- root is always statement sequence
- Statement sequence contains all statements as children
- operation is in the root, children are the operands
- first child of function contains arguments, second child the statement sequence
- conditional statements have two or three children: condition, if and optionally else

#### Constant folding (Arno)
- recursive function, only continues folding if all children have folded successfully
- Folds using a lambda a class can have als attribute

#### Symbol table (Basil)
- Tree of symbol tables -> testing in which scope we need to look
- There should be added that once a value is called in the scope it is created when running through the ast generation

#### Code generation (Basil)
- Also recursive
- output code is attribute of AST, each recursive function writes to this output
- function for getting a llvm variable of a node, which loads the variable into memory if required
- Functions of which the llvm code has the same structure have a get_llvm_template function, which gets filled in in the superclass (virtual functions)
- We should also note that autogenerated llvm variables are always preceded by a . instead of a letter, we do not use numbers because it vastly complicates the code

#### Benchmark (Arno)
- Test function compares output and return code with clang compiled code
- Semantic error tests try to catch the error type that's expected and compares the string version of this error with the expected output
- Many tests fail because ++ isn't implemented (since it was optional) -> but we fixed it right now not in the zip though
- Arrays aren't working yet, but we are working on it, so these tests aren’t in the 
- Function declaration c++ style also causes errors to fail: One function can be declared multiple times with different parameters
- comparisons are interpreted as float
- Definition in local scope not scope checked
- returnType mismatch not checked
- main not found not checked
- scan functions showed as succeeding but need to be tested manually :(

### Part 2 (Final Evaluation)
#### Introduction (Basil)
- We have chosen to translate llvm to mips
- this was easier to do because of not using the ast, and doing double work
- LLVM can be translated fast to mips, without too much hassle
#### Grammar (Arno)
- We have changed most of our c grammar because it was a mess as earlier said by Brentje
- We’ve  also made a new grammar for making a tree from the llvm code
- From the root (start_rule) you can go to a list of operations and after that your declarations
- An operation can be any of these, 
- most of the grammar rules explain itself 
- Then we have all the operations there are
- The grammar is just a generalization of the llvm code and is not that interesting to explain further
#### AST (Arno)
- The ast contains all the lines in llvm, it is directly a 1 to 1 translation
- Functions have a special representation in the ast
- In case of a definition these are the function arguments and the statement sequence
- In case of a function call we have the function arguments below it
- For a scanf and printf we do a separation of the string into the arguments in order to put the arguments passed through into the children like it is right there to be printed
- The ast is not deep at all so there are not a lot of things to take account for our llvm generation took all the hard work off our shoulders
#### Symbol table (Basil)
- We use the same symbol table as before but we tweaked the code slightly in order to accomodate for llvm
- Now we have a separate dot generation for the symbol table
- Global variables are in the root of the symbol table
- There is also a global table available which contains all the variables
- It can be generated after all the symbol tables have been linked, and will be generated when executing the function merge
#### Code generation (Basil)
- For the code generation we use separate files in order to keep the ast class clean
- It uses a visitor which traverses in preorder traversal, it is the same as reading the llvm code from left to right
- We translate each operation directly from the llvm code to mips
- We do this by loading each variable into the 0 and 1 register of its kind
- So in the t or f register depending on the value it is
- And then we store the values in that memory location of like in llvm described
- You can see in the global variables that there are quite a lot this is because these are all the llvm variables
- For every function we have a building stackframe and a destructing stackframe, which speaks for itself
#### Benchmark (Arno)
- The benchmark still fails on some tests but all are explainable
- There is still one test failing in semantic errors this is because we do not support -- and ++
- We also need to note that some of the benchmarks are modified because we do not support all the functionality, since some of it was optional
- There is also a massive improvement to the previous submission of our code because we have tweaked it such that the benchmarks will run
- This does not  mean we have hardcoded all the benchmarks to succeed
- There is also the thing of scan tests not being tested, they need to be done manually
- Both our comparison tests do not work, because we have a special implementation
- This means when we compare two variables/constants we keep them in their type and do not convert them to decimal
- We do this in order to not mess around with types, it is too much work that is not necessary in our case
- Since our tests use a standard compiler we can not change the format tag since it will still fail because the standard compiler will give 0 for the output of a float when it is a decimal
- SPIM does behave weird because on mips it should work all right if tested by hand
- Also our float to int conversion do not work since they are optional
- A lot of tests for C to LLVM are fixed
