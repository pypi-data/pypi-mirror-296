from depviz.parsers.requirements_parser import parse_requirements
from depviz.parsers.bazel_parser import parse_bazel_build
from depviz.parsers.package_json_parser import parse_package_json
from depviz.utils import find_internal_projects
import os
import logging


class DependencyGraph:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.internal_projects = find_internal_projects(root_dir)
        self.dependencies = {}  # {project_name: {'internal': [], 'external': []}}

    def collect_dependencies(self, project_path):
        deps = []
        files = os.listdir(project_path)
        if "requirements.txt" in files:
            deps.extend(
                parse_requirements(os.path.join(project_path, "requirements.txt"))
            )
        if "BUILD" in files or "BUILD.bazel" in files:
            bazel_file = "BUILD" if "BUILD" in files else "BUILD.bazel"
            deps.extend(parse_bazel_build(os.path.join(project_path, bazel_file)))
        if "package.json" in files:
            deps.extend(parse_package_json(os.path.join(project_path, "package.json")))
        return deps

    def render(self, output_file="dependency_graph", view=False, format="png"):
        from graphviz import Digraph

        dot = Digraph(comment="Monorepo Dependency Graph")
        dot.attr("node", shape="box")

        # Add internal project nodes
        for project in self.internal_projects.keys():
            dot.node(project, style="filled", fillcolor="lightblue")

        # Collect external dependencies
        external_deps = set()
        for deps in self.dependencies.values():
            external_deps.update(deps["external"])

        # Add external dependency nodes
        for dep in external_deps:
            dot.node(dep, style="filled", fillcolor="lightgrey")

        # Add edges for internal dependencies
        for project, deps in self.dependencies.items():
            for internal_dep in deps["internal"]:
                dot.edge(project, internal_dep)

            for external_dep in deps["external"]:
                dot.edge(project, external_dep, style="dashed")

        dot.format = format
        dot.render(output_file, view=view)

    def build_graph(self):
        for project_name, project_path in self.internal_projects.items():
            logging.info(f"Processing project: {project_name}")
            self.dependencies[project_name] = {"internal": [], "external": []}
            deps = self.collect_dependencies(project_path)
            self.dependencies[project_name]["internal"] = [
                dep for dep in deps if dep in self.internal_projects
            ]
            self.dependencies[project_name]["external"] = [
                dep for dep in deps if dep not in self.internal_projects
            ]
