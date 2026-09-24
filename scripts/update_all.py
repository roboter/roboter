"""
Master execution script for roboter GitHub Profile README generator.
Runs the entire update pipeline in sequential order.
"""

import sys
import os

# Ensure script directory is in sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import importlib.util

def run_step(module_name, func_name):
    module_path = os.path.join(script_dir, f"{module_name}.py")
    print(f"\n==========================================")
    print(f"Executing Step: {module_name}.py")
    print(f"==========================================")
    
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    func = getattr(module, func_name)
    func()

def main():
    steps = [
        ("1_fetch_repos", "fetch_repos"),
        ("2_process_forks", "process_forks"),
        ("3_find_screenshots", "find_screenshots"),
        ("4_fill_descriptions", "fill_descriptions"),
        ("5_build_readme", "build_readme"),
    ]
    
    for mod, func in steps:
        run_step(mod, func)
        
    print("\n[OK] All steps completed successfully! README.md is up to date.")

if __name__ == '__main__':
    main()
