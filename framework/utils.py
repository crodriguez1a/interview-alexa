import json
# import yaml


def from_yaml(filename):
    stream = open(filename, "r")
    # file = yaml.load_all(stream)

def from_json(filename):
    with open("{}.json".format(filename), "r") as f:
        return json.load(f)
