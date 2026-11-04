from tokens import Token

class LexerError(Exception): pass

class Lexer:
    KEYWORDS = {"let":"LET", "if":"IF", "else":"ELSE", "while":"WHILE",
                "true":"TRUE", "false":"FALSE", "null":"NULL",
                "and":"AND", "or":"OR", "not":"NOT", "print":"PRINT"}
    TWO = {"==", "!=", "<=", ">="}
    SINGLE = set("+-*/%=<>!(){}[],;")

    def __init__(self, source):
        self.source, self.pos, self.line, self.col = source, 0, 1, 1

    def peek(self, n=0):
        p = self.pos+n
        return self.source[p] if p < len(self.source) else "\0"

    def advance(self):
        ch = self.peek()
        self.pos += 1
        if ch == "\n": self.line, self.col = self.line+1, 1
        else: self.col += 1
        return ch

    def tokenize(self):
        out = []
        while self.peek() != "\0":
            ch = self.peek()
            if ch in " \t\r": self.advance(); continue
            if ch == "\n" or ch == ";":
                ln, cl = self.line, self.col
                self.advance(); out.append(Token("NEWLINE", "\\n", ln, cl)); continue
            if ch == "/" and self.peek(1) == "/":
                while self.peek() not in ("\n", "\0"): self.advance()
                continue
            if ch.isdigit():
                ln, cl, start = self.line, self.col, self.pos
                while self.peek().isdigit(): self.advance()
                if self.peek()=="." and self.peek(1).isdigit():
                    self.advance()
                    while self.peek().isdigit(): self.advance()
                raw = self.source[start:self.pos]
                out.append(Token("NUMBER", float(raw) if "." in raw else int(raw), ln, cl)); continue
            if ch.isalpha() or ch=="_":
                ln, cl, start = self.line, self.col, self.pos
                while self.peek().isalnum() or self.peek()=="_": self.advance()
                word = self.source[start:self.pos]
                out.append(Token(self.KEYWORDS.get(word, "IDENT"), word, ln, cl)); continue
            if ch in "\"'":
                ln, cl, quote = self.line, self.col, self.advance()
                chars=[]
                while self.peek() not in (quote, "\0"):
                    c=self.advance()
                    if c=="\\":
                        e=self.advance()
                        chars.append({"n":"\n","t":"\t","r":"\r","\\":"\\",'"':'"',"'":"'"}.get(e,e))
                    else: chars.append(c)
                if self.peek()=="\0": raise LexerError(f"Unterminated string at {ln}:{cl}")
                self.advance(); out.append(Token("STRING","".join(chars),ln,cl)); continue
            pair=ch+self.peek(1)
            if pair in self.TWO:
                ln,cl=self.line,self.col; self.advance(); self.advance()
                out.append(Token(pair,pair,ln,cl)); continue
            if ch in self.SINGLE:
                ln,cl=self.line,self.col; self.advance()
                out.append(Token(ch,ch,ln,cl)); continue
            raise LexerError(f"Unexpected character {ch!r} at {self.line}:{self.col}")
        out.append(Token("EOF",None,self.line,self.col))
        return out
