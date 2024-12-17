import argparse
import os
import shutil
import time

from templates.read import get_template_items, parse_template_items


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

    os.makedirs(project_final_path, exist_ok=False)

    files = get_template_items(args.template.lower())

    if not files:
        raise ValueError(f"Template {args.template} not exists.")

    in_files, ex_files = parse_template_items(files)

    print(f"Generating {args.template.upper()} template...")
    for file in in_files:
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

main()