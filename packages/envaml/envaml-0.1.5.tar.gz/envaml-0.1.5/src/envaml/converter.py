import re
import subprocess
import platform
import yaml


def flatten_dict(d, parent_key='', sep='_') -> dict:
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def resolve_value(value):
    if platform.system() == 'Windows':
        result = subprocess.run(
            [
                'wsl',
                'echo',
                value
            ],
            capture_output=True,
            text=True)
    else:
        result = subprocess.run(['echo', value], capture_output=True, text=True)
    return result.stdout.strip()


def write_env_file(filename, configs):
    with open(filename, 'w') as env:
        for i, (top_key, flattened_config) in enumerate(configs.items()):
            for key, value in flattened_config.items():
                if re.match(r'\$\(.*\)', str(value)):
                    value = resolve_value(value)
                env.write(f"{key}={value}\n")
            if i < len(configs) - 1:
                env.write("\n")


def convert_yaml_to_env(yaml_file, split_by_parent=False):
    with open(yaml_file, 'r') as stream:
        config = yaml.safe_load(stream)

    if split_by_parent:
        for top_key, sub_dict in config.items():
            flattened_config = flatten_dict(sub_dict, parent_key=top_key)
            write_env_file(f"{top_key}.env", {top_key: flattened_config})
    else:
        combined_config = {top_key: flatten_dict(sub_dict, parent_key=top_key)
                           for top_key, sub_dict in config.items()}
        write_env_file('.env', combined_config)
