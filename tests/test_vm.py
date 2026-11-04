import unittest
from contextlib import redirect_stdout
from io import StringIO
from main import compile_source
from vm import VirtualMachine
class VMTests(unittest.TestCase):
    def test_print(self):
        code,_=compile_source('print(2 + 3)')
        out=StringIO()
        with redirect_stdout(out):VirtualMachine(code).run()
        self.assertEqual(out.getvalue().strip(),"5")
if __name__=="__main__":unittest.main()
