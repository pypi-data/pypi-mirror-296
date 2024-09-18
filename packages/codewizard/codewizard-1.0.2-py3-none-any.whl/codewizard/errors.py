import click
import os

ERROR_LOG_FILE = os.path.expanduser('~/.codewizard/error.log')

@click.group()
def errors_cli():
    pass

@errors_cli.command()
def track():
    """Track and log errors"""
    click.echo("Tracking errors...")

    try:
        _simulate_error()
    except Exception as e:
        _log_error(str(e))
        click.echo(f"Error logged: {str(e)}")

def _simulate_error():
    raise Exception("This is a simulated error.")

def _log_error(message):
    with open(ERROR_LOG_FILE, 'a') as f:
        f.write(f"{message}\n")
