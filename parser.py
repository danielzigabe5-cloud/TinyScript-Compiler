import ast_nodes as A

class ParserError(Exception): pass

class Parser:
    def __init__(self,tokens): self.tokens,self.i=tokens,0
    def peek(self): return self.tokens[self.i]
    def check(self,t): return self.peek().type==t
    def advance(self):
        tok=self.peek()
        if tok.type!="EOF": self.i+=1
        return tok
    def match(self,*types):
        if self.check_any(*types): self.advance(); return True
        return False
    def check_any(self,*types): return self.peek().type in types
    def consume(self,t,msg):
        if self.check(t): return self.advance()
        x=self.peek(); raise ParserError(f"{msg} at {x.line}:{x.column}; got {x.type}")
    def separators(self):
        while self.match("NEWLINE"): pass
    def parse(self):
        statements=[]; self.separators()
        while not self.check("EOF"):
            statements.append(self.statement())
            if not self.check("EOF") and not self.check("}"):
                if not self.match("NEWLINE"):
                    x=self.peek(); raise ParserError(f"Expected newline or ';' at {x.line}:{x.column}")
                self.separators()
        return A.Program(statements)
    def statement(self):
        if self.match("LET"):
            name=self.consume("IDENT","Expected variable name").value
            self.consume("=","Expected '='")
            return A.Let(name,self.expression())
        if self.match("PRINT"):
            self.consume("(","Expected '(' after print")
            e=self.expression(); self.consume(")","Expected ')'")
            return A.Print(e)
        if self.match("IF"):
            self.consume("(","Expected '('"); c=self.expression(); self.consume(")","Expected ')'")
            yes=self.block(); separator_start=self.i; self.separators()
            if self.match("ELSE"):
                no=self.block()
            else:
                self.i=separator_start
                no=[]
            return A.If(c,yes,no)
        if self.match("WHILE"):
            self.consume("(","Expected '('"); c=self.expression(); self.consume(")","Expected ')'")
            return A.While(c,self.block())
        if self.check("IDENT"):
            start=self.i
            target=self.postfix()
            if self.match("="):
                value=self.expression()
                if isinstance(target,A.Variable):
                    return A.Assign(target.name,value)
                if isinstance(target,A.Index):
                    return A.IndexAssign(target.collection,target.index,value)
                x=self.tokens[start]
                raise ParserError(f"Invalid assignment target at {x.line}:{x.column}")
            self.i=start
        return A.ExprStmt(self.expression())
    def block(self):
        self.consume("{","Expected '{'"); body=[]; self.separators()
        while not self.check("}") and not self.check("EOF"):
            body.append(self.statement())
            if not self.check("}") and not self.match("NEWLINE"):
                x=self.peek(); raise ParserError(f"Expected newline in block at {x.line}:{x.column}")
            self.separators()
        self.consume("}","Expected '}'")
        return body
    def expression(self): return self.or_expr()
    def binary_chain(self,sub,types):
        e=sub()
        while self.match(*types): op=self.tokens[self.i-1].type; e=A.Binary(e,op,sub())
        return e
    def or_expr(self): return self.binary_chain(self.and_expr,("OR",))
    def and_expr(self): return self.binary_chain(self.equality,("AND",))
    def equality(self): return self.binary_chain(self.comparison,("==","!="))
    def comparison(self): return self.binary_chain(self.term,("<","<=",">",">="))
    def term(self): return self.binary_chain(self.factor,("+","-"))
    def factor(self): return self.binary_chain(self.unary,("*","/","%"))
    def unary(self):
        if self.match("!","NOT","-"): return A.Unary(self.tokens[self.i-1].type,self.unary())
        return self.postfix()
    def postfix(self):
        e=self.primary()
        while self.match("["):
            idx=self.expression(); self.consume("]","Expected ']'")
            e=A.Index(e,idx)
        return e
    def primary(self):
        if self.match("NUMBER","STRING"): return A.Literal(self.tokens[self.i-1].value)
        if self.match("TRUE"): return A.Literal(True)
        if self.match("FALSE"): return A.Literal(False)
        if self.match("NULL"): return A.Literal(None)
        if self.match("IDENT"):
            name=self.tokens[self.i-1].value
            if name=="len" and self.match("("):
                value=self.expression()
                self.consume(")","Expected ')' after len argument")
                return A.Length(value)
            return A.Variable(name)
        if self.match("("):
            e=self.expression(); self.consume(")","Expected ')'"); return e
        if self.match("["):
            items=[]
            if not self.check("]"):
                items.append(self.expression())
                while self.match(","): items.append(self.expression())
            self.consume("]","Expected ']'"); return A.ListExpr(items)
        x=self.peek(); raise ParserError(f"Expected expression at {x.line}:{x.column}")
