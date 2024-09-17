import click
import json
import os
import pyperclip

SNIPPETS_FILE = os.path.expanduser('~/.codewizard/snippets.json')

@click.group()
def snippet_cli():
    pass

@snippet_cli.command()
def list():
    """List all code snippets"""
    snippets = _load_snippets()
    if not snippets:
        click.echo("No snippets found.")
        return
    
    for snippet in snippets:
        click.echo(f"Name: {snippet['name']}, Language: {snippet['language']}, Tags: {', '.join(snippet['tags'])}")
        click.echo(f"Code:\n{snippet['code']}\n")

@snippet_cli.command()
@click.option('--tag', prompt='Enter tag to search', help='Tag to search for snippets')
def find(tag):
    """Find and optionally copy snippets by tag"""
    snippets = _load_snippets()
    tagged_snippets = [s for s in snippets if tag in s['tags']]
    
    if not tagged_snippets:
        click.echo(f"No snippets found with tag '{tag}'.")
        return

    for snippet in tagged_snippets:
        click.echo(f"Name: {snippet['name']}, Language: {snippet['language']}, Tags: {', '.join(snippet['tags'])}")
        click.echo(f"Code:\n{snippet['code']}\n")
        if click.confirm('Do you want to copy this snippet to the clipboard?'):
            pyperclip.copy(snippet['code'])
            click.echo('Snippet copied to clipboard.')

@snippet_cli.command()
def add():
    """Add a new code snippet"""
    name = click.prompt('Enter snippet name')
    language = click.prompt('Enter snippet language')
    code = click.edit()
    tags = click.prompt('Enter tags (comma-separated)').split(',')

    snippet = {
        'name': name,
        'language': language,
        'code': code,
        'tags': tags
    }

    snippets = _load_snippets()
    snippets.append(snippet)
    _save_snippets(snippets)

    click.echo(f"Added snippet: {name}")

def _load_snippets():
    if os.path.exists(SNIPPETS_FILE):
        with open(SNIPPETS_FILE, 'r') as f:
            return json.load(f)
    return []

def _save_snippets(snippets):
    with open(SNIPPETS_FILE, 'w') as f:
        json.dump(snippets, f, indent=4)

if __name__ == '__main__':
    snippet_cli()
