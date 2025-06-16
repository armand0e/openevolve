import argparse
import time
import os
import yaml # Ensure pyyaml is available

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enhanced Dummy OpenEvolve Runner")
    parser.add_argument("initial_program", help="Path to the initial program")
    parser.add_argument("evaluation_file", help="Path to the evaluation script")
    parser.add_argument("--config", help="Path to the config YAML file", required=True)
    parser.add_argument("--iterations", type=int, help="Number of iterations, may override config")
    parser.add_argument("--output_path", help="Directory for outputs, may override config")

    args = parser.parse_args()

    effective_iterations = None
    effective_output_path = args.output_path
    llm_api_base_from_config = None
    llm_model_from_config = None

    print(f"EnhancedDummyOpenEvolve: Called with raw args: {args}")
    print(f"EnhancedDummyOpenEvolve: Initial program: {args.initial_program}")
    print(f"EnhancedDummyOpenEvolve: Evaluation file: {args.evaluation_file}")

    try:
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
            print(f"EnhancedDummyOpenEvolve: Successfully loaded config file: {args.config}")
            if config.get('llm'):
                llm_api_base_from_config = config['llm'].get('api_base')
                llm_model_from_config = config['llm'].get('primary_model')

            print(f"EnhancedDummyOpenEvolve: LLM API Base from config: {llm_api_base_from_config}")
            print(f"EnhancedDummyOpenEvolve: LLM Model from config: {llm_model_from_config}")

            if 'max_iterations' in config:
                effective_iterations = config['max_iterations']
            if not effective_output_path and config.get('output_path_in_config'): # Fictional config key for testing
                effective_output_path = config['output_path_in_config']
    except Exception as e:
        print(f"EnhancedDummyOpenEvolve: Error - Could not read/parse config {args.config}: {e}")

    if args.iterations is not None:
        effective_iterations = args.iterations

    if effective_iterations is None:
        effective_iterations = 5 # Absolute fallback

    if effective_output_path is None:
        effective_output_path = "./openevolve_output_dummy_enhanced_default"

    print(f"EnhancedDummyOpenEvolve: Effective iterations: {effective_iterations}")
    print(f"EnhancedDummyOpenEvolve: Effective output path: {effective_output_path}")

    os.makedirs(effective_output_path, exist_ok=True)

    # Simulate checkpoint structure
    final_checkpoint_dir_name = f"checkpoint_{str(effective_iterations).zfill(3)}"
    final_checkpoint_path = os.path.join(effective_output_path, "checkpoints", final_checkpoint_dir_name)
    os.makedirs(final_checkpoint_path, exist_ok=True)

    best_program_content = f"# Dummy best program after {effective_iterations} iterations.\n"
    best_program_content += f"# Configured API base: {llm_api_base_from_config}\n"
    best_program_content += f"# Configured Model: {llm_model_from_config}\n"
    best_program_content += "print('Hello from dummy ENHANCED evolved code!')\n"

    with open(os.path.join(final_checkpoint_path, "best_program.py"), "w") as f:
        f.write(best_program_content)

    print(f"EnhancedDummyOpenEvolve: Starting evolution for {effective_iterations} iterations...")
    for i in range(1, int(effective_iterations) + 1):
        print(f"Iteration {i}/{effective_iterations} completed. Best score: {i*0.1:.2f}")
        if i % 2 == 0 or i == int(effective_iterations):
             print(f"EnhancedDummyOpenEvolve: Checkpoint for iteration {i} saved in {final_checkpoint_path}.")
        time.sleep(0.01)

    print("EnhancedDummyOpenEvolve: Evolution finished.")
