import re


def parse_bazel_build(file_path):
    dependencies = []
    with open(file_path, "r") as f:
        content = f.read()
        # Extract deps from py_library, py_binary, etc.
        pattern = r"deps\s*=\s*\[([^\]]*)\]"
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
        for match in matches:
            deps = re.findall(r'"([^"]+)"', match)
            dependencies.extend(deps)
    return dependencies
