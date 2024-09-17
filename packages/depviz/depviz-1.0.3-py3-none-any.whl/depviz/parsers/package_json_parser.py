import json


def parse_package_json(file_path):
    dependencies = []
    with open(file_path, "r") as f:
        data = json.load(f)
        for dep_type in ["dependencies", "devDependencies", "peerDependencies"]:
            deps = data.get(dep_type, {})
            dependencies.extend(deps.keys())
    return dependencies
