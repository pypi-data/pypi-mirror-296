import click
import logging
from depviz.graph import DependencyGraph


@click.command()
@click.option("--path", default=".", help="Path to the monorepo root directory")
@click.option(
    "--output", default="dependency_graph", help="Output file name without extension"
)
@click.option("--format", default="png", help="Output file format (e.g., png, pdf)")
@click.option("--view", is_flag=True, help="Open the output file after generation")
@click.option("--verbose", is_flag=True, help="Enable verbose output")
def main(path, output, format, view, verbose=False):
    """Generate a high-level dependency graph for a monorepo."""
    if verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

    logging.info(f"Scanning monorepo at {path}...")
    graph = DependencyGraph(path)
    graph.build_graph()
    logging.info(f"Generating dependency graph...")
    graph.render(output_file=output, view=view, format=format)
    logging.info(f"Dependency graph saved as {output}.{format}")
