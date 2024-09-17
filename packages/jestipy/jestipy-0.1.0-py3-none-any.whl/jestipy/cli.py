import argparse
import os
import runpy  
import sys

def run_tests_in_file(file_path):
    print(f"Running tests in: {file_path}")
    try:
        runpy.run_path(file_path, run_name="__main__")
    except Exception as e:
        print(f"Error while running {file_path}: {e}")

def run_cli():
    parser = argparse.ArgumentParser(description="Run the test suite")
    parser.add_argument("path", help="The test file or directory to run (e.g., tests/ or tests/test_example.py)")
    args = parser.parse_args()

    if os.path.isdir(args.path):
        for root, dirs, files in os.walk(args.path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    run_tests_in_file(file_path)
    elif os.path.isfile(args.path) and args.path.endswith(".py"):
        run_tests_in_file(args.path)
    else:
        print(f"Error: No valid Python file or directory found at {args.path}")
        sys.exit(1)

if __name__ == "__main__":
    run_cli()
