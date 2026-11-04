import unittest
from main import compile_source
class CompilerTests(unittest.TestCase):
    def test_halt(self):
        code,_=compile_source("let x = 1")
        self.assertEqual(code[-1][0],"HALT")
if __name__=="__main__":unittest.main()
