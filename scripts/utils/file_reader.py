from pathlib import Path

PROJECT_PATH = Path(__file__).parents[2]


def get_list_from_resources(filename):
    file = PROJECT_PATH / "resources/{}".format(filename)
    with open(file, 'r') as f:
        data = f.readlines()
    return [line.strip('\n') for line in data]
