"""
findmod.py

A utility script to recursively scan a directory for Python files and extract all imported modules.
It uses the `ast` module to parse Python source files and collect both `import` and `from ... import ...` statements.

Functions:
- find_modules_in_directory(directory): Walks the directory tree using os.walk and collects imported modules.
- find_modules_in_directory2(directory): Uses glob to recursively find Python files and collects imported modules.
- save_modules_to_file(modules, filename): Saves the set of found modules to a text file, one per line.

Usage:
- Set the `directory_path` variable to the target directory.
- The script prints all found modules and saves them to "modules_used.txt".

Note:
- Syntax errors in Python files are reported and skipped.
"""

import ast
import glob
import os


def find_modules_in_directory(directory):
    modules = set()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    try:
                        tree = ast.parse(f.read(), filename=file_path)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    modules.add(alias.name)
                            elif isinstance(node, ast.ImportFrom):
                                modules.add(node.module)
                    except SyntaxError:
                        print(f"Syntax error in file {file_path}, skipping.")

    return modules


def find_modules_in_directory2(directory):
    modules = set()

    # recursively get all files under the folder
    files = [f for f in glob.glob(directory + "/**/*.py", recursive=True)]
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                tree = ast.parse(f.read(), filename=file_path)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            modules.add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        modules.add(node.module)
            except SyntaxError:
                print(f"Syntax error in file {file_path}, skipping.")

    return modules


def save_modules_to_file(modules, filename):
    """Save the set of modules to a text file, one per line."""
    with open(filename, "w", encoding="utf-8") as f:
        for module in sorted(modules):
            f.write(f"{module}\n")


if "__name__" == "__main__":
    directory_path: str = "../."
    modules_used = find_modules_in_directory2(directory_path)
    print("Modules used in the directory:")
    for module in modules_used:
        print(module)

    # Save to file
    save_modules_to_file(modules_used, "modules_used.txt")
    print("Modules saved to modules_used.txt")
