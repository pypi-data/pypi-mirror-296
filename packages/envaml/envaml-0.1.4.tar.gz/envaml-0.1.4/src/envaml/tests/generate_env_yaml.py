import yaml
import random
import string


def random_string(length=6):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_nested_dict(depth, max_depth, child_count):
    if depth == max_depth or child_count <= 0:
        return {random_string(): random_string()}

    nested_dict = {}
    num_children = random.randint(1, min(3, child_count))

    for _ in range(num_children):
        key = random_string()
        if random.choice([True, False]) and depth < max_depth - 1:
            nested_dict[key] = generate_nested_dict(depth + 1, max_depth,
                                                    child_count // num_children)
        else:
            nested_dict[key] = random_string()

    return nested_dict


def generate_yaml(top_level_count=20, max_depth=5, child_count=30):
    yaml_data = {}
    for _ in range(top_level_count):
        top_key = random_string()
        yaml_data[top_key] = generate_nested_dict(0, max_depth, child_count)
    return yaml_data


def generate_yaml_file(top_level_count=20, max_depth=5, child_count=30):
    yaml_file_name = 'env.yaml'
    yaml_data = generate_yaml(top_level_count, max_depth, child_count)
    with open('env.yaml', 'w') as file:
        yaml.dump(yaml_data, file)
    return yaml_file_name
