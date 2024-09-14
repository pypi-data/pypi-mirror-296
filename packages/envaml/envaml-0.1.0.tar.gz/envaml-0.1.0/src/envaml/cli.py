import click
from .converter import convert_yaml_to_env

@click.command()
@click.argument('yaml_file')
@click.argument('env_file')
def cli(yaml_file, env_file):
    """Convert YAML_FILE to ENV_FILE."""
    convert_yaml_to_env(yaml_file, env_file)
    click.echo(f"Converted {yaml_file} to {env_file}")

if __name__ == '__main__':
    cli()