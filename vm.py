class VMError(Exception): pass
class VirtualMachine:
    def __init__(self,code):
        self.code=code; self.stack=[]; self.globals={}; self.scopes=[self.globals]; self.ip=0
    def pop(self):
        if not self.stack: raise VMError("Stack underflow")
        return self.stack.pop()
    def run(self):
        while self.ip<len(self.code):
            op,arg=self.code[self.ip]; self.ip+=1
            if op=="HALT":break
            if op=="CONST":self.stack.append(arg)
            elif op=="LOAD":
                for scope in reversed(self.scopes):
                    if arg in scope:
                        self.stack.append(scope[arg])
                        break
                else:raise VMError(f"Undefined variable '{arg}'")
            elif op=="DECLARE":
                if arg in self.scopes[-1]:
                    raise VMError(f"Variable '{arg}' already declared in this scope")
                self.scopes[-1][arg]=self.pop()
            elif op=="STORE":
                value=self.pop()
                for scope in reversed(self.scopes):
                    if arg in scope:
                        scope[arg]=value
                        break
                else:raise VMError(f"Undefined variable '{arg}'")
            elif op=="ENTER_SCOPE":self.scopes.append({})
            elif op=="EXIT_SCOPE":
                if len(self.scopes)==1:raise VMError("Cannot exit the global scope")
                self.scopes.pop()
            elif op=="POP":self.pop()
            elif op=="PRINT":print(self.pop())
            elif op=="BUILD_LIST":
                vals=self.stack[-arg:] if arg else []
                if arg:del self.stack[-arg:]
                self.stack.append(vals)
            elif op=="GET_INDEX":
                idx=self.pop(); obj=self.pop()
                if not isinstance(idx,int) or isinstance(idx,bool):
                    raise VMError("Index must be an integer")
                try:self.stack.append(obj[idx])
                except (IndexError,TypeError,KeyError) as e:raise VMError(f"Invalid index: {e}")
            elif op=="SET_INDEX":
                value=self.pop(); idx=self.pop(); obj=self.pop()
                if not isinstance(idx,int) or isinstance(idx,bool):
                    raise VMError("Index must be an integer")
                try:obj[idx]=value
                except (IndexError,TypeError,KeyError) as e:raise VMError(f"Cannot assign at index: {e}")
            elif op=="LENGTH":
                value=self.pop()
                if not isinstance(value,(str,list)):
                    raise VMError("len() expects a string or list")
                self.stack.append(len(value))
            elif op=="JUMP":self.ip=arg
            elif op=="JUMP_IF_FALSE":
                if not self.pop():self.ip=arg
            elif op in ("NEG","NOT"):
                x=self.pop();self.stack.append(-x if op=="NEG" else not x)
            else:
                b=self.pop();a=self.pop()
                try:
                    f={"ADD":lambda:a+b,"SUB":lambda:a-b,"MUL":lambda:a*b,"DIV":lambda:a/b,
                       "MOD":lambda:a%b,"EQ":lambda:a==b,"NE":lambda:a!=b,"LT":lambda:a<b,
                       "LE":lambda:a<=b,"GT":lambda:a>b,"GE":lambda:a>=b,
                       "AND":lambda:bool(a) and bool(b),"OR":lambda:bool(a) or bool(b)}[op]
                    self.stack.append(f())
                except (TypeError,ZeroDivisionError) as e:raise VMError(f"{op} failed: {e}")
        return self.globals
