import os
import logging


def find_internal_projects(root_dir):
    internal_projects = {}
    excluded_dirs = {
        ".git",
        "venv",
        "env",
        "node_modules",
        "build",
        "dist",
        "__pycache__",
    }
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude unnecessary directories
        dirnames[:] = [d for d in dirnames if d not in excluded_dirs]
        project_files = {
            "requirements.txt",
            "setup.py",
            "BUILD",
            "BUILD.bazel",
            "package.json",
        }
        if project_files.intersection(filenames):
            project_name = os.path.basename(dirpath)
            internal_projects[project_name] = dirpath
    return internal_projects


def get_package_info_from_setup(setup_py_path):
    import ast

    with open(setup_py_path, "r") as f:
        node = ast.parse(f.read(), filename=setup_py_path)

    package_info = {}
    for elem in node.body:
        if isinstance(elem, ast.Expr) and isinstance(elem.value, ast.Call):
            if getattr(elem.value.func, "id", None) == "setup":
                for keyword in elem.value.keywords:
                    if keyword.arg == "name" or keyword.arg == "version":
                        value = keyword.value
                        if isinstance(value, ast.Str):
                            # For Python < 3.8
                            package_info[keyword.arg] = value.s
                        elif isinstance(value, ast.Constant):
                            # For Python >= 3.8
                            package_info[keyword.arg] = value.value
                        else:
                            try:
                                package_info[keyword.arg] = ast.literal_eval(value)
                            except Exception as e:
                                logging.warning(
                                    f"Could not evaluate {keyword.arg} in {setup_py_path}: {e}"
                                )
    return package_info if "name" in package_info else None
