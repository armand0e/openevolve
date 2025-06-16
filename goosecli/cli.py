import click
import os
from .evolve import run_evolve

@click.group()
def cli():
    """Goose CLI - Your AI Software Engineering Assistant"""
    pass

@cli.command()
@click.argument('filepath', type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.option('--evaluator', 'evaluator_path', required=True, type=click.Path(exists=True, dir_okay=False, resolve_path=True), help='Path to the evaluator Python script.')
@click.option('--goal', type=str, help='Natural language description of the evolution goal.')
@click.option('--openevolve-config', 'openevolve_config_path', type=click.Path(exists=True, dir_okay=False, resolve_path=True), help='Path to a custom OpenEvolve YAML config file.')
@click.option('--iterations', type=int, help='Number of iterations for OpenEvolve. Overrides value in config if --openevolve-config is also used.')
@click.option('--output-dir', 'output_dir_override', type=click.Path(file_okay=False, resolve_path=True), help='Specific directory for OpenEvolve outputs. If unset, OpenEvolve uses its default (often ./openevolve_output).')
def evolve(filepath, evaluator_path, goal, openevolve_config_path, iterations, output_dir_override):
    """Evolves the specified Python file using OpenEvolve."""
    run_evolve(filepath, evaluator_path, goal, openevolve_config_path, iterations, output_dir_override)

if __name__ == '__main__':
    cli()
