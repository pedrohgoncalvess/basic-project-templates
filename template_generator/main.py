import argparse
import inspect
import os
import shutil
import time
import sys

import pyperclip

sys.path.append('..')

from template_generator.templates.read import get_template_items, parse_template_items, get_possible_templates
from template_generator.services import * # Necessary for import custom functions


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Python projects with template.")
    parser.add_argument("--name", type=str, required=True)
    parser.add_argument("--path", type=str, default=".",
                        help="Path to create project.")
    parser.add_argument("--template", type=str, default="default", required=False,
                        help="Template to use.")

    args = parser.parse_args()

    project_name = args.name
    project_path = os.path.abspath(args.path)

    project_final_path = f"{project_path}\\{project_name}"
    
    if os.path.exists(project_final_path):
        raise FileExistsError(f"Path {project_final_path} already exists.")

    files = get_template_items(args.template.lower())

    if not files:
        existing_templates = get_possible_templates()
        raise ValueError(f"Template {args.template} not exists.\nExiting templates are: {', '.join(existing_templates)}")
    
    type_, args1, args2 = parse_template_items(files)
    
    print(f"Generating {project_name} project...")

    if type_ == "function":
        func_name = args1
        func_args = args2

        tt_func_args = [
            arg
            .replace("$$project_name$$", project_name)
            .replace("$$project_final_path$$", project_final_path) for arg in func_args
        ]

        func = globals()[func_name]

        sig = inspect.signature(func)
        required_params = 0

        for param in sig.parameters.values():
            if param.default == inspect.Parameter.empty and param.kind not in (
                    inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                required_params += 1

        func(*tt_func_args)


    if type_ == "normal":
        in_files = args1
        ex_files = args2

        for file in in_files:
            os.makedirs(project_final_path, exist_ok=True)
            if isinstance(file, dict):
                original_name = list(file.keys())[0]
                new_name = list(file.values())[0]

                # TODO: Centralize project path in a variable
                if os.path.isdir(f"template_generator\\files\\{original_name}"):
                    shutil.copytree(f"template_generator\\files\\{original_name}", f"{project_final_path}\\{new_name}")
                else:
                    shutil.copy(f"template_generator\\files\\{original_name}", f"{project_final_path}\\{new_name}")
                continue

            if os.path.isdir(f"template_generator\\files\\{file}"):
                shutil.copytree(f"template_generator\\files\\{file}", f"{project_final_path}\\{file}")
            else:
                shutil.copy(f"template_generator\\files\\{file}", f"{project_final_path}\\{file}")

        if ex_files:
            print("Excluding unnecessary folders and files.")
            for ex_file in ex_files:
                if os.path.isdir(f"{project_final_path}\\{ex_file}"):
                    attempt = 0
                    try:
                        shutil.rmtree(f"{project_final_path}\\{ex_file}")
                    except PermissionError:
                        if attempt >= 3:
                            raise PermissionError(f"Could not delete folder: {ex_file}")
                        else:
                            attempt += 1
                            time.sleep(2)

                else:
                    os.remove(f"{project_final_path}\\{ex_file}")

    print(f"Project: {project_name} created.\nProject path: {project_final_path}.\nTemplate used: {args.template}.")
    print(f"Project config was copied to the copy board.")
    pyperclip.copy(f"""cd "{project_final_path}"\nmake setup""")
    
    
if __name__ == '__main__':
    main()