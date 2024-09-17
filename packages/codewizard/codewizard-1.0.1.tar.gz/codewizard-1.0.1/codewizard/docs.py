import click
import os
import glob

@click.group()
def docs_cli():
    pass

@docs_cli.command()
@click.option('--path', prompt='Project path', help='Path to the project')
@click.option('--output', default='docs', help='Output directory for the documentation')
def generate(path, output):
    """Generate documentation for a project"""
    if not os.path.exists(path):
        click.echo(f"Project path {path} does not exist.")
        return

    if not os.path.exists(output):
        os.makedirs(output)

    doc_files = []
    for filename in glob.iglob(f'{path}/**/*.py', recursive=True):
        with open(filename, 'r') as f:
            content = f.read()
            docstring = _extract_docstring(content)
            if docstring:
                doc_files.append((filename, docstring))

    if not doc_files:
        click.echo("No docstrings found in the project.")
        return

    for filename, docstring in doc_files:
        output_file = os.path.join(output, os.path.basename(filename) + ".md")
        with open(output_file, 'w') as f:
            f.write(f"# Documentation for {filename}\n\n")
            f.write(docstring)
            f.write("\n")
    
    click.echo(f"Documentation generated in {output} directory.")

def _extract_docstring(content):
    lines = content.split('\n')
    docstring_lines = []
    in_docstring = False

    for line in lines:
        if line.strip().startswith(('"""', "'''")):
            if in_docstring:
                docstring_lines.append(line)
                break
            else:
                in_docstring = True
        
        if in_docstring:
            docstring_lines.append(line)
    
    return "\n".join(docstring_lines) if docstring_lines else ""
