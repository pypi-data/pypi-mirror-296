import os

def find_internal_projects(root_dir):
    internal_projects = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        project_files = {'requirements.txt', 'setup.py', 'BUILD', 'BUILD.bazel', 'package.json'}
        if project_files.intersection(filenames):
            project_name = os.path.basename(dirpath)
            internal_projects[project_name] = dirpath
    return internal_projects