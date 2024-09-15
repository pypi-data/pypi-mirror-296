import click
from envaml.converter import convert_yaml_to_env
from envaml.tests.generate_env_yaml import generate_yaml_file
import paprika


@click.group()
def cli():
    pass


@cli.command()
@click.argument('yaml_file', default='env.yaml', required=False)
@click.option('-p', '--parent', is_flag=True,
              help="Split into separate files for each parent.")
def convert(yaml_file, parent):
    """Convert YAML_FILE to .env files."""
    convert_yaml_to_env(yaml_file, split_by_parent=parent)
    if parent:
        click.echo(f"Converted {yaml_file} to individual files by top-level keys.")
    else:
        click.echo(f"Converted {yaml_file} to .env")


@cli.command()
@click.option('-p', '--parent', is_flag=True,
              help="Split into separate files for each parent.")
def test(parent):
    """Generate test env.yaml and convert to .env files."""
    yaml_file = generate_yaml_file()

    paprika.timeit(lambda: convert_yaml_to_env(yaml_file, split_by_parent=parent))()

    if parent:
        click.echo(
            "Generated test env.yaml and converted to individual files by top-level keys.")
    else:
        click.echo("Generated test env.yaml and converted to .env")
