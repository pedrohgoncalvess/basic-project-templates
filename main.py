import argparse
import os
import shutil
import time
import subprocess

from templates.read import get_template_items, parse_template_items, get_possible_templates


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
    
    in_files, ex_files = parse_template_items(files)
    
    print(f"Generating {project_name} project...")
    for file in in_files:
        if type(file) is tuple:
            tt_commands = [
                    c.replace("$$project_name$$", project_name).replace("$$project_final_path$$", project_final_path) for c in file[1]
            ]
            match file[0]:
                case "command":
                    subprocess.run(tt_commands)
                    continue
        
        os.makedirs(project_final_path, exist_ok=True)
        if type(file) is dict:
            original_name = list(file.keys())[0]
            new_name = list(file.values())[0]

            if os.path.isdir(f"files\\{original_name}"):
                shutil.copytree(f"files\\{original_name}", f"{project_final_path}\\{new_name}")
            else:
                shutil.copy(f"files\\{original_name}", f"{project_final_path}\\{new_name}")
            continue
        
        if os.path.isdir(f"files\\{file}"):
            shutil.copytree(f"files\\{file}", f"{project_final_path}\\{file}")
        else:
            shutil.copy(f"files\\{file}", f"{project_final_path}\\{file}")

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