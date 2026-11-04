import ast_nodes as A
from symbol_table import SymbolTable

class SemanticError(Exception): pass
class SemanticAnalyzer:
    def __init__(self): self.table=SymbolTable()
    def analyze(self,program):
        for stmt in program.statements: self.statement(stmt)
    def expression(self,n):
        if isinstance(n,(A.Literal,)): return
        if isinstance(n,A.Variable):
            try: self.table.assign_check(n.name)
            except ValueError as e: raise SemanticError(str(e))
        elif isinstance(n,A.ListExpr):
            for x in n.items:self.expression(x)
        elif isinstance(n,A.Index): self.expression(n.collection); self.expression(n.index)
        elif isinstance(n,A.Length): self.expression(n.value)
        elif isinstance(n,A.Unary): self.expression(n.right)
        elif isinstance(n,A.Binary): self.expression(n.left); self.expression(n.right)
    def statement(self,n):
        if isinstance(n,A.Let):
            self.expression(n.value)
            try:self.table.declare(n.name)
            except ValueError as e:raise SemanticError(str(e))
        elif isinstance(n,A.Assign):
            try:self.table.assign_check(n.name)
            except ValueError as e:raise SemanticError(str(e))
            self.expression(n.value)
        elif isinstance(n,A.IndexAssign):
            self.expression(n.collection)
            self.expression(n.index)
            self.expression(n.value)
        elif isinstance(n,A.Print): self.expression(n.value)
        elif isinstance(n,A.ExprStmt): self.expression(n.value)
        elif isinstance(n,A.If):
            self.expression(n.condition)
            self.table.push()
            for s in n.then_body:self.statement(s)
            self.table.pop()
            self.table.push()
            for s in n.else_body:self.statement(s)
            self.table.pop()
        elif isinstance(n,A.While):
            self.expression(n.condition); self.table.push()
            for s in n.body:self.statement(s)
            self.table.pop()
