import unittest
from click.testing import CliRunner
from codewizard.cli import main

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def test_snippets_command(self):
        result = self.runner.invoke(main, ['snippets'])
        self.assertEqual(result.exit_code, 0)

    def test_docs_command(self):
        result = self.runner.invoke(main, ['docs'])
        self.assertEqual(result.exit_code, 0)

    def test_errors_command(self):
        result = self.runner.invoke(main, ['errors'])
        self.assertEqual(result.exit_code, 0)

    def test_quality_command(self):
        result = self.runner.invoke(main, ['quality'])
        self.assertEqual(result.exit_code, 0)

if __name__ == '__main__':
    unittest.main()
