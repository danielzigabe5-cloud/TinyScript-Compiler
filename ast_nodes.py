from dataclasses import dataclass
class Node: pass
@dataclass
class Program(Node): statements:list
@dataclass
class Let(Node): name:str; value:Node
@dataclass
class Assign(Node): name:str; value:Node
@dataclass
class IndexAssign(Node): collection:Node; index:Node; value:Node
@dataclass
class Print(Node): value:Node
@dataclass
class If(Node): condition:Node; then_body:list; else_body:list
@dataclass
class While(Node): condition:Node; body:list
@dataclass
class ExprStmt(Node): value:Node
@dataclass
class Literal(Node): value:object
@dataclass
class Variable(Node): name:str
@dataclass
class ListExpr(Node): items:list
@dataclass
class Index(Node): collection:Node; index:Node
@dataclass
class Length(Node): value:Node
@dataclass
class Unary(Node): op:str; right:Node
@dataclass
class Binary(Node): left:Node; op:str; right:Node
