# evaluator_script.py
import importlib.util
import os
import sys

def evaluate(program_path):
    print(f"Evaluator: Attempting to evaluate {program_path}")
    try:
        module_name = os.path.splitext(os.path.basename(program_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, program_path)
        if spec is None or spec.loader is None:
            print(f"Evaluator: Could not create module spec for {program_path}")
            return {"fitness": 0.0, "error": "Could not load module spec"}

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        if hasattr(module, 'main_logic'):
            result = module.main_logic()
            # Example: Higher fitness if it returns the expected 'evolved' value
            if result == 42: # Expecting an evolved function
                return {"fitness": 1.0, "correctness": 1.0, "value": result}
            else:
                return {"fitness": 0.1, "correctness": 0.0, "value": result}
        else:
            return {"fitness": 0.0, "error": "main_logic function not found in evolved code"}

    except Exception as e:
        print(f"Evaluator: Error during evaluation of {program_path}: {str(e)}")
        return {"fitness": 0.0, "error": str(e)}

if __name__ == '__main__':
    if len(sys.argv) > 1:
        metrics = evaluate(sys.argv[1])
        print(f"Evaluation metrics: {metrics}")
    else:
        print("Usage: python evaluator_script.py <path_to_program_to_evaluate>")
