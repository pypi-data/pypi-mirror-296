# import click
from click import echo, command, argument, option
from envaml.converter import convert_yaml_to_env
from paprika import timeit


# import glob
# import os
# import yaml


# def concatenate_yaml(files):
#     concatenated_data = []
#
#     for file in files:
#         with open(file, 'r') as f:
#             data = yaml.safe_load(f)
#             if data is not None:
#                 concatenated_data.append(data)
#
#     return yaml.dump_all(concatenated_data)


@command()
@argument('yaml_file', default='env.yaml', required=False)
# @click.argument('env_file', default='.env', required=False)
@option('-p', '--parent', is_flag=True,
              help="Split into separate files for each parent.")
@timeit
def cli(yaml_file, parent):
    """Convert YAML_FILE to .env files."""
    convert_yaml_to_env(yaml_file, split_by_parent=parent)
    if parent:
        echo(f"Converted {yaml_file} to individual files by top-level keys.")
    else:
        echo(f"Converted {yaml_file} to .env")
