# TinyScript Dynamic Language Compiler
Group 3 – Track C | Python implementation

## Folder structure
- `tokens.py`: token data structure
- `lexer.py`: scanner / lexical analysis
- `ast_nodes.py`: AST node definitions
- `parser.py`: recursive-descent parser
- `symbol_table.py`: nested symbol table
- `semantic.py`: semantic checks
- `compiler.py`: AST-to-bytecode compiler
- `vm.py`: bytecode virtual machine
- `main.py`: command-line entry point
- `examples/`: sample `.ts` and `.tiny` programs
- `tests/`: unit tests for compiler phases

## Requirements
Python 3.10+; no external packages.

## Run
From the project root folder:
```powershell
python main.py examples/hello.ts
python main.py examples/hello.ts --bytecode
python main.py examples/hello.ts --save-bytecode
python main.py examples/hello.ts --save-bytecode build/program.bc
python main.py examples/hello.ts --tokens
python -m unittest discover -s tests -v
```

## Language sample
```text
let name = "Abel"
let values = [10, 20, 30]
print("Hello " + name)
print(values[1])
values[0] = 100
print(len(name))
if (values[0] > 5) {
    print("greater")
} else {
    print("smaller")
}
```

## Grammar overview
```text
program    -> statement*
statement  -> "let" IDENT "=" expression
            | IDENT "=" expression
            | IDENT ("[" expression "]")+ "=" expression
            | "print" "(" expression ")"
            | "if" "(" expression ")" block ("else" block)?
            | "while" "(" expression ")" block
block      -> "{" statement* "}"
expression -> logic_or
logic_or   -> logic_and ("or" logic_and)*
logic_and  -> equality ("and" equality)*
equality   -> comparison (("==" | "!=") comparison)*
comparison -> term (("<" | "<=" | ">" | ">=") term)*
term       -> factor (("+" | "-") factor)*
factor     -> unary (("*" | "/" | "%") unary)*
unary      -> ("!" | "not" | "-") unary | postfix
postfix    -> primary ("[" expression "]")*
primary    -> NUMBER | STRING | true | false | null | IDENT | "len(" expression ")"
            | "(" expression ")" | "[" (expression ("," expression)*)? "]"
```

TinyScript supports dynamic variables, numbers, strings, lists and list/string indexing, list element assignment, string concatenation, and `len(value)` for strings and lists. Variables declared inside `if`/`else`/`while` blocks are local to the block; assignment to an existing outer variable updates it.

`--save-bytecode [PATH]` writes the generated instruction listing to a `.bc` file. When `PATH` is omitted, the source filename is used with a `.bc` extension. Errors are reported as lexical, syntax, semantic, runtime, or file errors.
