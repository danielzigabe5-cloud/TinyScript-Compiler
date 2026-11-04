import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from main import compile_source, main
from semantic import SemanticError
from vm import VMError, VirtualMachine


class FeatureTests(unittest.TestCase):
    def run_source(self, source):
        code, _ = compile_source(source)
        output = StringIO()
        with redirect_stdout(output):
            VirtualMachine(code).run()
        return output.getvalue().splitlines()

    def test_list_index_assignment(self):
        self.assertEqual(
            self.run_source("let numbers = [1, 2]\nnumbers[0] = 100\nprint(numbers[0])"),
            ["100"],
        )

    def test_string_length_concatenation_and_indexing(self):
        self.assertEqual(
            self.run_source(
                'let word = "Tiny"\nprint(len(word))\nprint(word + "Script")\nprint(word[1])'
            ),
            ["4", "TinyScript", "i"],
        )

    def test_block_scope_shadowing_and_outer_assignment(self):
        self.assertEqual(
            self.run_source(
                "let value = 1\n"
                "if (true) {\n"
                " let value = 2\n"
                " print(value)\n"
                "}\n"
                "if (true) {\n"
                " value = 3\n"
                "}\n"
                "print(value)"
            ),
            ["2", "3"],
        )

    def test_block_local_is_not_visible_after_block(self):
        with self.assertRaises(SemanticError):
            compile_source("if (true) {\n let local = 1\n}\nprint(local)")

    def test_runtime_errors_are_clear(self):
        code, _ = compile_source("print(1 / 0)")
        with self.assertRaisesRegex(VMError, "DIV failed"):
            VirtualMachine(code).run()

    def test_save_bytecode_to_bc_file(self):
        with tempfile.TemporaryDirectory() as directory:
            source_path = Path(directory) / "program.tiny"
            bytecode_path = Path(directory) / "program.bc"
            source_path.write_text("print(1 + 2)", encoding="utf-8")
            output = StringIO()
            with patch.object(sys, "argv", ["main.py", str(source_path), "--save-bytecode"]), redirect_stdout(output):
                main()
            self.assertEqual(output.getvalue().strip(), "3")
            bytecode = bytecode_path.read_text(encoding="utf-8")
            self.assertIn("ADD", bytecode)
            self.assertTrue(bytecode.rstrip().endswith("HALT"))

    def test_cli_classifies_language_errors(self):
        cases = (
            ("print(@)", "Lexical error:"),
            ("print(", "Syntax error:"),
            ("print(missing)", "Semantic error:"),
            ("print(1 / 0)", "Runtime error:"),
        )
        with tempfile.TemporaryDirectory() as directory:
            source_path = Path(directory) / "invalid.tiny"
            for source, expected_message in cases:
                source_path.write_text(source, encoding="utf-8")
                output = StringIO()
                with patch.object(sys, "argv", ["main.py", str(source_path)]), redirect_stdout(output):
                    with self.assertRaises(SystemExit) as result:
                        main()
                self.assertEqual(result.exception.code, 1)
                self.assertIn(expected_message, output.getvalue())


if __name__ == "__main__":
    unittest.main()
