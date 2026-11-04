import unittest
from lexer import Lexer
from parser import Parser
class ParserTests(unittest.TestCase):
    def test_parse_program(self):
        p=Parser(Lexer("let x = 1\nprint(x)").tokenize()).parse()
        self.assertEqual(len(p.statements),2)
if __name__=="__main__":unittest.main()
