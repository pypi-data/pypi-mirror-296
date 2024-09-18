import unittest
import os
import json
from click.testing import CliRunner
from codewizard.snippets import snippet_cli, SNIPPETS_FILE

class TestSnippetsCLI(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()
        if os.path.exists(SNIPPETS_FILE):
            os.remove(SNIPPETS_FILE)

    def tearDown(self):
        if os.path.exists(SNIPPETS_FILE):
            os.remove(SNIPPETS_FILE)

    def test_list_snippets_no_snippets(self):
        result = self.runner.invoke(snippet_cli, ['list'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('No snippets found.', result.output)

    def test_add_snippet(self):
        result = self.runner.invoke(snippet_cli, ['add'], input='Test Snippet\nPython\nprint("Hello, World!")\ntest, example\n')
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Added snippet: Test Snippet', result.output)
        with open(SNIPPETS_FILE, 'r') as f:
            snippets = json.load(f)
        self.assertEqual(len(snippets), 1)
        self.assertEqual(snippets[0]['name'], 'Test Snippet')

    def test_list_snippets_with_snippets(self):
        self.runner.invoke(snippet_cli, ['add'], input='Test Snippet\nPython\nprint("Hello, World!")\ntest, example\n')
        result = self.runner.invoke(snippet_cli, ['list'])
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Name: Test Snippet', result.output)
        self.assertIn('Language: Python', result.output)
        self.assertIn('Tags: test, example', result.output)
        self.assertIn('Code:\nprint("Hello, World!")', result.output)

if __name__ == '__main__':
    unittest.main()
