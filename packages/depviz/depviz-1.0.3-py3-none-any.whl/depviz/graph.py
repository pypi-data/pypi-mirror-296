import os
from depviz.parsers.requirements_parser import parse_all_requirements
from depviz.utils import get_package_info_from_setup
import logging


class DependencyGraph:
    def __init__(self, root_dir, services_dir, packages_dir, requirements_pattern):
        self.root_dir = root_dir
        self.services_dir = os.path.join(root_dir, services_dir)
        self.packages_dir = os.path.join(root_dir, packages_dir)
        self.requirements_pattern = requirements_pattern
        self.internal_packages = self.find_internal_packages()
        self.dependencies = self.collect_dependencies()

    def find_internal_packages(self):
        internal_packages = {}
        for dirpath, dirnames, filenames in os.walk(self.packages_dir):
            if "setup.py" in filenames:
                setup_py_path = os.path.join(dirpath, "setup.py")
                package_info = get_package_info_from_setup(setup_py_path)
                if package_info:
                    package_name = package_info["name"]
                    version = package_info.get("version", "unknown")
                    internal_packages[package_name] = {
                        "path": dirpath,
                        "version": version,
                    }
        logging.info(f"Found internal packages: {list(internal_packages.keys())}")
        return internal_packages

    def collect_dependencies(self):
        dependencies = {}
        # Collect dependencies for each service
        for service_name in os.listdir(self.services_dir):
            service_path = os.path.join(self.services_dir, service_name)
            if os.path.isdir(service_path):
                logging.info(f"Processing service: {service_name}")
                deps = parse_all_requirements(
                    service_path, self.requirements_pattern, self.root_dir
                )
                dependencies[service_name] = deps
        return dependencies

    def build_graph(self):
        from graphviz import Digraph

        dot = Digraph(comment="Monorepo Dependency Graph")
        dot.attr("node", shape="box")

        # Add nodes for services
        for service in self.dependencies.keys():
            dot.node(service, fillcolor="lightblue", style="filled")

        # Add nodes and edges for dependencies
        for service, deps in self.dependencies.items():
            for dep_name, dep_version, dep_type in deps:
                if dep_type == "internal":
                    # Internal package
                    version_label = f"{dep_name}\n(v{dep_version})"
                    dot.node(
                        dep_name,
                        label=version_label,
                        fillcolor="lightgreen",
                        style="filled",
                    )
                    dot.edge(service, dep_name)
                else:
                    # External package
                    version_label = (
                        f"{dep_name} {dep_version}" if dep_version else dep_name
                    )
                    dot.node(
                        dep_name,
                        label=version_label,
                        fillcolor="lightgrey",
                        style="filled",
                    )
                    dot.edge(service, dep_name, style="dashed")

        self.graph = dot

    def render(self, output_file="dependency_graph", view=False, format="png"):
        self.graph.format = format
        self.graph.render(output_file, view=view)
