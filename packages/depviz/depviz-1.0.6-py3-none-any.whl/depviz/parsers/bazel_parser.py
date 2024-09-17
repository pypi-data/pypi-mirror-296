import re
import os


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


def parse_bazel_dependencies(service_path):
    """Parse both BUILD and .bzl files for dependencies."""
    dependencies = []

    # Parse BUILD file
    build_file = os.path.join(service_path, "BUILD")
    if os.path.exists(build_file):
        dependencies.extend(parse_bazel_build(build_file))

    # Parse defs.bzl or other .bzl files
    for file_name in os.listdir(service_path):
        if file_name.endswith(".bzl"):
            bzl_file_path = os.path.join(service_path, file_name)
            dependencies.extend(parse_bazel_defs(bzl_file_path))

    return dependencies
