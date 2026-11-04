import unittest
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer,SemanticError
class SemanticTests(unittest.TestCase):
    def test_undefined(self):
        p=Parser(Lexer("print(nope)").tokenize()).parse()
        with self.assertRaises(SemanticError):SemanticAnalyzer().analyze(p)
if __name__=="__main__":unittest.main()
