import unittest
from lexer import Lexer
class LexerTests(unittest.TestCase):
    def test_tokens(self):
        ts=Lexer('let x = 12').tokenize()
        self.assertEqual([t.type for t in ts[:4]],["LET","IDENT","=","NUMBER"])
if __name__=="__main__":unittest.main()
