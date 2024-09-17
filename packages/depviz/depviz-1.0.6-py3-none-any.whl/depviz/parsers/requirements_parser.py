import os
import re
import glob
from depviz.utils import get_package_info_from_setup


def parse_requirements(file_path, base_dir):
    """Parse a requirements.txt file and extract dependencies."""
    dependencies = []
    if not os.path.exists(file_path):
        return dependencies
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("-r"):
                # Handle recursive includes
                included_file = line.split(" ", 1)[1]
                included_file_path = os.path.join(
                    os.path.dirname(file_path), included_file
                )
                dependencies.extend(parse_requirements(included_file_path, base_dir))
            elif line.startswith("-e") or line.startswith("--editable"):
                # Editable install (internal package)
                path = line.split(" ", 1)[1]
                pkg_path = os.path.normpath(
                    os.path.join(os.path.dirname(file_path), path)
                )
                setup_py = os.path.join(pkg_path, "setup.py")
                if os.path.exists(setup_py):
                    package_info = get_package_info_from_setup(setup_py)
                    if package_info:
                        dependencies.append(
                            (package_info["name"], package_info["version"], "internal")
                        )
            else:
                # External package
                match = re.match(r"^([a-zA-Z0-9_\-\.]+)([<>=!]=?[\d\.]+)?", line)
                if match:
                    package = match.group(1)
                    version = match.group(2) if match.group(2) else ""
                    dependencies.append((package, version, "external"))
    return dependencies


def parse_all_requirements(service_path, requirements_pattern, base_dir):
    """Find and parse all requirements files."""
    dependencies = []
    requirements_files = glob.glob(os.path.join(service_path, requirements_pattern))
    for req_file in requirements_files:
        dependencies.extend(parse_requirements(req_file, base_dir))
    return dependencies
