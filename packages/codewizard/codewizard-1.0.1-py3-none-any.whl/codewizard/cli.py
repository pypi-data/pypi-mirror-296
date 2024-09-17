import click
from codewizard.snippets import snippet_cli
from codewizard.docs import docs_cli
from codewizard.quality import quality_cli
from codewizard.extensions.extensions import load_custom_commands

@click.group()
def main():
    pass

# Register subcommands
main.add_command(snippet_cli, "snippets")
main.add_command(docs_cli, "docs")
main.add_command(quality_cli, "quality")

# Load custom commands
load_custom_commands(main)

@main.command()
def help():
    """Show all commands available under codewizard"""
    click.echo('Available commands:')
    click.echo('  snippets   Manage code snippets')
    click.echo('  docs       Generate documentation for a project')
    click.echo('  quality    Check code quality for a specific file')
    click.echo('  help       Show all commands available under codewizard')

if __name__ == '__main__':
    main()
