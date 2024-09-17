import click
import logging
import os
import yaml
from depviz.graph import DependencyGraph


@click.command()
@click.option("--config", default=None, help="Path to the configuration file")
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

    # Load configuration from file if provided
    if config:
        config_path = os.path.abspath(config)
        if not os.path.exists(config_path):
            logging.error(f"Configuration file not found: {config_path}")
            return
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)
        # Only override options not set via command-line
        if path == ".":
            path = config_data.get("path", path)
        if services_dir == "services/":
            services_dir = config_data.get("services_dir", services_dir)
        if packages_dir == "packages/python/":
            packages_dir = config_data.get("packages_dir", packages_dir)
        if requirements_pattern == "requirements*.txt":
            requirements_pattern = config_data.get(
                "requirements_pattern", requirements_pattern
            )
        if output == "dependency_graph":
            output = config_data.get("output", output)
        if format == "png":
            format = config_data.get("format", format)
        if not view:
            view = config_data.get("view", view)
        if not verbose:
            verbose = config_data.get("verbose", verbose)

    # Set logging level after merging configurations
    if verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    logging.info(f"Scanning monorepo at {path}...")
    graph = DependencyGraph(
        root_dir=path,
        services_dir=services_dir,
        packages_dir=packages_dir,
        requirements_pattern=requirements_pattern,
    )
    graph.build_graph()
    logging.info(f"Generating dependency graph...")
    graph.render(output_file=output, view=view, format=format)
    logging.info(f"Dependency graph saved as {output}.{format}")


if __name__ == "__main__":
    main()
