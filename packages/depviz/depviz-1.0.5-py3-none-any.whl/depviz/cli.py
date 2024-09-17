import click
import logging
import os
import yaml
from depviz.graph import DependencyGraph


@click.command()
@click.option("--config", default=None, help="Path to the configuration file")
@click.option(
    "--parser",
    default="bazel",
    type=click.Choice(["bazel", "requirements", "package_json"]),
    help="Choose the parser type: bazel or requirements",
)
@click.option("--path", default=".", help="Path to the monorepo root directory")
@click.option(
    "--services-dir",
    default="services/",
    help="Relative path to the services directory",
)
@click.option(
    "--packages-dir",
    default="packages/python/",
    help="Relative path to the packages directory",
)
@click.option(
    "--requirements-pattern",
    default="requirements*.txt",
    help="Pattern for requirements files",
)
@click.option(
    "--output", default="dependency_graph", help="Output file name without extension"
)
@click.option("--format", default="png", help="Output file format (e.g., png, pdf)")
@click.option("--view", is_flag=True, help="Open the output file after generation")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def main(
    config,
    parser,
    path,
    services_dir,
    packages_dir,
    requirements_pattern,
    output,
    format,
    view,
    verbose,
):
    """Generate a dependency graph for a monorepo."""

    if verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    # Load configuration from file if provided
    if config:
        config_path = os.path.abspath(config)
        if not os.path.exists(config_path):
            logging.error(f"Configuration file not found: {config_path}")
            return
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)
        # Override command-line options with config file settings
        path = config_data.get("path", path)
        services_dir = config_data.get("services_dir", services_dir)
        packages_dir = config_data.get("packages_dir", packages_dir)
        requirements_pattern = config_data.get(
            "requirements_pattern", requirements_pattern
        )
        output = config_data.get("output", output)
        format = config_data.get("format", format)
        view = config_data.get("view", view)
        verbose = config_data.get("verbose", verbose)

    logging.info(f"Scanning monorepo at {path}...")

    # Initialize the dependency graph with the selected parser
    graph = DependencyGraph(
        root_dir=path,
        services_dir=services_dir,
        packages_dir=packages_dir,
        requirements_pattern=requirements_pattern,
        parser=parser,  # Pass parser choice to the graph
    )
    graph.build_graph()
    logging.info(f"Generating dependency graph...")
    graph.render(output_file=output, view=view, format=format)
    logging.info(f"Dependency graph saved as {output}.{format}")


if __name__ == "__main__":
    main()
