import argparse
import inspect
import os
import shutil
import sys
import yaml

import pyperclip

sys.path.append('..')

from template_generator.templates.read import get_template_items, parse_template_items, get_possible_templates
from template_generator.manipulate_files import copy_files, copy_project_files
from template_generator.custom import * # Necessary for import custom functions


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Python projects with template.")
    parser.add_argument("--name", type=str, required=False)
    parser.add_argument("--path", type=str, default=None,
                        help="Path to create project.", required=False)
    parser.add_argument("--template", type=str, default="default", required=False,
                        help="Template to use.")
    parser.add_argument("--custom", type=str, default=None, required=False,
                        help="Custom files to use.")

    args = parser.parse_args()  #TODO: Separate this main function in two functions. one for custom.yaml and another for template.

    custom_yaml_file = os.path.abspath(args.custom) if args.custom else None

    if custom_yaml_file:
        if not custom_yaml_file.endswith(".yaml"):
            raise ValueError("Custom file must be .yaml.")

        if not os.path.exists(custom_yaml_file):
            raise FileNotFoundError(f"Path {custom_yaml_file} not exists.")

    project_name = args.name
    project_path = os.path.abspath(args.path) if args.path else None

    if not custom_yaml_file:
        if not project_name:
            raise ValueError("Project name is required. Use the --name argument.")

        if not project_path:
            raise ValueError("Project path is required. Use the --path argument.")

    project_final_path = f"{project_path}/{project_name}"
    template_generator_path = os.path.abspath(f"template_generator/files")

    if os.path.exists(project_final_path):
        raise FileExistsError(f"Path {project_final_path} already exists.")

    if custom_yaml_file:
        with open(custom_yaml_file, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        projects = config.get("projects")

        if not projects:
            raise ValueError("The custom YAML must have the key projects. Read the example (custom.example.yaml) in the documentation for a better understanding.")

        for project in projects:
            project_path = args.path if args.path else project["path"]
            project_name = args.name if args.name else project["name"]
            project_final_path = f"{project_path}\\{project_name}"

            project_files = project["files"]
            add_files: list[str] = project_files["add"]
            rem_files: list[str] = project_files.get("remove", [])

            print(f"Generating {project_name} project...")
            _, tt_add_files, _ = parse_template_items(add_files)
            try:
                copy_project_files(project_final_path, template_generator_path, tt_add_files, rem_files)

                print(f"Project {project_name.upper()} created.\nProject path: {project_final_path}.\nUsing custom configuration.")
                print(f"Project config was copied to the copy board.")
                pyperclip.copy(f"""cd "{project_final_path}"\nmake setup""")
            except Exception as error:
                print(f"Project {project_name.upper()} cannot be created.")
                print(f"Reason: {error}.")
                print(f"Removing traces...")
                shutil.rmtree(project_final_path)

    else:
        files = get_template_items(args.template.lower())

        if not files:
            existing_templates = get_possible_templates()
            raise ValueError(f"Template {args.template} not exists.\nExisting templates are: {', '.join(existing_templates)}")

        type_, args1, args2 = parse_template_items(files)

        print(f"Generating {project_name} project...")

        try:
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
                copy_project_files(project_final_path, template_generator_path, in_files, ex_files)

            print(f"Project {project_name.upper()} created.\nProject path: {project_final_path}.\nUsing custom configuration.")
            print(f"Project config was copied to the copy board.")
            pyperclip.copy(f"""cd "{project_final_path}"\nmake setup""")
        except Exception as error:
            print(f"Project {project_name.upper()} cannot be created.")
            print(f"Reason: {error}.")
            print(f"Removing traces...")
            shutil.rmtree(project_final_path)
    
    
if __name__ == '__main__':
    main()