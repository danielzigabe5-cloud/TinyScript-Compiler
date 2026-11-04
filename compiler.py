import ast_nodes as A
class Compiler:
    def __init__(self): self.code=[]
    def emit(self,op,arg=None): self.code.append([op,arg]); return len(self.code)-1
    def patch(self,i,target): self.code[i][1]=target
    def compile(self,p):
        for s in p.statements:self.statement(s)
        self.emit("HALT")
        return self.code
    def statement(self,n):
        if isinstance(n,A.Let): self.expression(n.value); self.emit("DECLARE",n.name)
        elif isinstance(n,A.Assign): self.expression(n.value); self.emit("STORE",n.name)
        elif isinstance(n,A.IndexAssign):
            self.expression(n.collection); self.expression(n.index); self.expression(n.value)
            self.emit("SET_INDEX")
        elif isinstance(n,A.Print): self.expression(n.value); self.emit("PRINT")
        elif isinstance(n,A.ExprStmt): self.expression(n.value); self.emit("POP")
        elif isinstance(n,A.If):
            self.expression(n.condition); jf=self.emit("JUMP_IF_FALSE")
            self.emit("ENTER_SCOPE")
            for s in n.then_body:self.statement(s)
            self.emit("EXIT_SCOPE")
            if n.else_body:
                je=self.emit("JUMP")
                self.patch(jf,len(self.code))
                self.emit("ENTER_SCOPE")
                for s in n.else_body:self.statement(s)
                self.emit("EXIT_SCOPE")
                self.patch(je,len(self.code))
            else:self.patch(jf,len(self.code))
        elif isinstance(n,A.While):
            start=len(self.code); self.expression(n.condition); out=self.emit("JUMP_IF_FALSE")
            self.emit("ENTER_SCOPE")
            for s in n.body:self.statement(s)
            self.emit("EXIT_SCOPE")
            self.emit("JUMP",start); self.patch(out,len(self.code))
    def expression(self,n):
        if isinstance(n,A.Literal):self.emit("CONST",n.value)
        elif isinstance(n,A.Variable):self.emit("LOAD",n.name)
        elif isinstance(n,A.ListExpr):
            for x in n.items:self.expression(x)
            self.emit("BUILD_LIST",len(n.items))
        elif isinstance(n,A.Index):self.expression(n.collection);self.expression(n.index);self.emit("GET_INDEX")
        elif isinstance(n,A.Length):self.expression(n.value);self.emit("LENGTH")
        elif isinstance(n,A.Unary):
            self.expression(n.right);self.emit({"-":"NEG","!":"NOT","NOT":"NOT"}[n.op])
        elif isinstance(n,A.Binary):
            self.expression(n.left);self.expression(n.right)
            mapping={"+":"ADD","-":"SUB","*":"MUL","/":"DIV","%":"MOD","==":"EQ","!=":"NE",
                     "<":"LT","<=":"LE",">":"GT",">=":"GE","AND":"AND","OR":"OR"}
            self.emit(mapping[n.op])
