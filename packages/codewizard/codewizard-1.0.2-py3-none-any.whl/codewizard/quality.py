import click
import subprocess
import sys

@click.group()
def quality_cli():
    pass

@quality_cli.command()
@click.option('--file', prompt='File to check', help='File to check for quality')
def check(file):
    """Check code quality for a specific file"""
    if not _is_pylint_installed():
        _install_pylint()

    result = subprocess.run([sys.executable, '-m', 'pylint', file], capture_output=True, text=True)
    if result.returncode == 0:
        click.echo(f"File {file} passed all checks.")
    else:
        click.echo(f"Issues found in file {file}:\n{result.stdout}")

    score = _extract_score(result.stdout)
    if score is not None:
        click.echo(f"Quality score: {score}/10")

def _is_pylint_installed():
    try:
        subprocess.run([sys.executable, '-m', 'pylint', '--version'], capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

def _install_pylint():
    click.echo("pylint is not installed. Installing it now...")
    result = subprocess.run([sys.executable, '-m', 'pip', 'install', 'pylint'], capture_output=True, text=True)
    if result.returncode == 0:
        click.echo("pylint installed successfully.")
    else:
        click.echo(f"Failed to install pylint:\n{result.stderr}")
        sys.exit(1)

def _extract_score(output):
    for line in output.split('\n'):
        if line.strip().startswith('Your code has been rated at'):
            parts = line.strip().split(' ')
            score = parts[-1].split('/')[0]
            return score
    return None

if __name__ == '__main__':
    quality_cli()
