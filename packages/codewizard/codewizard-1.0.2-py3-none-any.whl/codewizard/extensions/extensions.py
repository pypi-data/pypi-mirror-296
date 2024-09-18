import importlib.util
import os
import click

def load_custom_commands(cli):
    extensions_path = os.path.expanduser('~/.codewizard/extensions/')
    if not os.path.exists(extensions_path):
        os.makedirs(extensions_path)

    for file in os.listdir(extensions_path):
        if file.endswith('.py'):
            module_name = file[:-3]
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(extensions_path, file))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, 'register_commands'):
                module.register_commands(cli)


def register_commands(cli):
    @cli.command()
    @click.argument('csv_file')
    @click.argument('json_file')
    def convert_csv_to_json(csv_file, json_file):
        import csv
        import json

        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        with open(json_file, 'w') as f:
            json.dump(rows, f, indent=4)

        print(f"Converted {csv_file} to {json_file}")
