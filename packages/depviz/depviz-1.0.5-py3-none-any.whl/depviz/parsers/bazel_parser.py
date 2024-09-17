import re


def parse_bazel_build(build_file_path):
    """Parse a Bazel BUILD file and extract dependencies."""
    dependencies = []
    with open(build_file_path, "r") as f:
        content = f.read()
        # Look for dependencies in deps = [...]
        deps_matches = re.findall(r"deps\s*=\s*\[(.*?)\]", content, re.DOTALL)
        for match in deps_matches:
            # Extract each dependency from the deps list
            deps = re.findall(r'"([^"]+)"', match)
            dependencies.extend(deps)
    return dependencies


def parse_bazel_defs(bzl_file_path):
    """Parse a .bzl file and extract dependencies."""
    dependencies = []
    with open(bzl_file_path, "r") as f:
        content = f.read()
        # Similar parsing logic to find deps in .bzl files
        deps_matches = re.findall(r"deps\s*=\s*\[(.*?)\]", content, re.DOTALL)
        for match in deps_matches:
            deps = re.findall(r'"([^"]+)"', match)
            dependencies.extend(deps)
    return dependencies
