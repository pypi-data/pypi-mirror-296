from depviz.parsers.bazel_parser import parse_bazel_build, parse_bazel_defs
from depviz.parsers.requirements_parser import parse_all_requirements
import os
import logging


class DependencyGraph:
    def __init__(
        self, root_dir, services_dir, packages_dir, requirements_pattern, parser
    ):
        self.root_dir = root_dir
        self.services_dir = os.path.join(root_dir, services_dir)
        self.packages_dir = os.path.join(root_dir, packages_dir)
        self.requirements_pattern = requirements_pattern
        self.internal_packages = self.find_internal_packages()
        self.parser_type = parser  # bazel or requirements
        self.dependencies = self.collect_dependencies()

    def find_internal_packages(self):
        """Find all internal packages."""
        internal_packages = {}
        for dirpath, dirnames, filenames in os.walk(self.packages_dir):
            if "BUILD" in filenames or "defs.bzl" in filenames:
                package_name = os.path.basename(dirpath)
                internal_packages[package_name] = dirpath
        return internal_packages

    def collect_dependencies(self):
        """Collect dependencies based on the selected parser."""
        if self.parser_type == "bazel":
            return self.collect_bazel_dependencies()
        else:
            return self.collect_requirements_dependencies()

    def collect_bazel_dependencies(self):
        """Collect dependencies from Bazel BUILD files and .bzl files."""
        dependencies = {}
        # Collect dependencies for each service
        for service_name in os.listdir(self.services_dir):
            service_path = os.path.join(self.services_dir, service_name)
            if os.path.isdir(service_path):
                logging.info(f"Processing service: {service_name}")
                # Check for BUILD or defs.bzl files in the service
                build_file = os.path.join(service_path, "BUILD")
                defs_file = os.path.join(service_path, "defs.bzl")

                if os.path.exists(build_file):
                    deps = parse_bazel_build(build_file)
                elif os.path.exists(defs_file):
                    deps = parse_bazel_defs(defs_file)
                else:
                    deps = []

                # Process dependencies (internal or external)
                for dep in deps:
                    if dep.startswith("//packages/python/"):
                        package_name = dep.split("/")[-1]
                        package_path = self.internal_packages.get(package_name)
                        if package_path:
                            dependencies[service_name] = (
                                self.check_internal_package_requirements(package_path)
                            )
        return dependencies

    def collect_requirements_dependencies(self):
        """Collect dependencies from requirements files across the monorepo."""
        dependencies = {}
        # Collect dependencies for each service
        for service_name in os.listdir(self.services_dir):
            service_path = os.path.join(self.services_dir, service_name)
            if os.path.isdir(service_path):
                logging.info(f"Processing service: {service_name}")
                # Parse requirements.txt or other matching files
                additional_deps = parse_all_requirements(
                    service_path, self.requirements_pattern, self.root_dir
                )
                dependencies[service_name] = additional_deps
        return dependencies

    def check_internal_package_requirements(self, package_path):
        """Check an internal package for additional Python dependencies."""
        return parse_all_requirements(
            package_path, self.requirements_pattern, self.root_dir
        )

    def build_graph(self):
        from graphviz import Digraph

        dot = Digraph(comment="Monorepo Dependency Graph")
        dot.attr("node", shape="box")

        # Add nodes for services and dependencies
        for service, deps in self.dependencies.items():
            dot.node(service, fillcolor="lightblue", style="filled")
            for dep in deps:
                dep_name = dep[0] if isinstance(dep, tuple) else dep
                dot.node(dep_name, fillcolor="lightgreen", style="filled")
                dot.edge(service, dep_name)

        self.graph = dot

    def render(self, output_file="dependency_graph", view=False, format="png"):
        self.graph.format = format
        self.graph.render(output_file, view=view)
