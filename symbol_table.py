class SymbolTable:
    def __init__(self): self.scopes=[{}]
    def push(self): self.scopes.append({})
    def pop(self): self.scopes.pop()
    def declare(self,name):
        if name in self.scopes[-1]: raise ValueError(f"Variable '{name}' already declared in this scope")
        self.scopes[-1][name]="dynamic"
    def exists(self,name): return any(name in scope for scope in reversed(self.scopes))
    def assign_check(self,name):
        if not self.exists(name): raise ValueError(f"Variable '{name}' used before declaration")
