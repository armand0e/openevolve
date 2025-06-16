import subprocess
import os
import yaml
import click # click is a dependency, ensure it's available

DEFAULT_ITERATIONS = 50
DEFAULT_LLM_API_BASE = "http://localhost:11434/v1" # Changed for direct Ollama
DEFAULT_LLM_MODEL = "codellama:7b-instruct"

def run_evolve(filepath, evaluator_path, goal, openevolve_config_path, iterations, output_dir_override):
    # File existence for filepath and evaluator_path is handled by click options in cli.py

    effective_output_dir_msg = output_dir_override if output_dir_override else "./openevolve_output (openevolve's default)"

    if output_dir_override:
        os.makedirs(output_dir_override, exist_ok=True)
        click.echo(f"OpenEvolve output will be directed to: {output_dir_override}")
    else:
        click.echo(f"OpenEvolve output directory will be its default (likely near the target file or current working directory).")

    actual_openevolve_config_path = openevolve_config_path

    if not actual_openevolve_config_path:
        config_save_dir = output_dir_override if output_dir_override else "."
        os.makedirs(config_save_dir, exist_ok=True)

        generated_config_filename = "goose_generated_openevolve_config.yaml"
        actual_openevolve_config_path = os.path.join(config_save_dir, generated_config_filename)

        current_iterations = iterations if iterations is not None else DEFAULT_ITERATIONS

        config_data = {
            "max_iterations": current_iterations,
            "llm": {
                "api_base": DEFAULT_LLM_API_BASE,
                "primary_model": DEFAULT_LLM_MODEL,
            },
            "database": {
                "population_size": 50
            },
            "evaluator": {
                "enable_artifacts": True
            }
        }
        with open(actual_openevolve_config_path, 'w') as f:
            yaml.dump(config_data, f)
        click.echo(f"Generated OpenEvolve config: {actual_openevolve_config_path}")

    cmd = ["python", "openevolve_run_dummy_enhanced.py", filepath, evaluator_path] # Changed to enhanced dummy
    cmd.extend(["--config", actual_openevolve_config_path])

    if iterations is not None:
        cmd.extend(["--iterations", str(iterations)])

    if output_dir_override:
        cmd.extend(["--output_path", output_dir_override])

    click.echo(f"Executing command: {' '.join(cmd)}")
    if goal:
        click.echo(f"Evolution Goal: {goal}")

    click.echo("Starting OpenEvolve process...")

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        for line in process.stdout:
            click.echo(line, nl=False)
        process.wait()

        if process.returncode == 0:
            click.echo("\nOpenEvolve process finished successfully.")
            click.echo(f"Please find outputs, checkpoints, and the best program in the output directory (see logs from openevolve, nominally: {effective_output_dir_msg}).")
            click.echo("The best program is typically found in a subdirectory like: <output_dir>/checkpoints/checkpoint_XXX/best_program.py")
        else:
            click.echo(f"\nOpenEvolve process failed with exit code {process.returncode}.", err=True)

    except FileNotFoundError:
        click.echo("\nError: `openevolve_run_dummy_enhanced.py` not found. Ensure it is in the current working directory.", err=True)
    except Exception as e:
        click.echo(f"\nAn error occurred while running OpenEvolve: {e}", err=True)
