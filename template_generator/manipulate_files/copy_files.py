import os
import shutil
import time


def copy_project_files(project_final_path: str, template_generator_files_path: str, add_files: list[tuple[str] | str], rem_files: list[str]):
    for file in add_files:
        os.makedirs(project_final_path, exist_ok=True)
        if isinstance(file, tuple):
            original_name = file[0]
            new_name = file[1]

            if os.path.isdir(f"{template_generator_files_path}/{original_name}"):
                shutil.copytree(f"{template_generator_files_path}/{original_name}", f"{project_final_path}/{new_name}")
            else:
                shutil.copy(f"{template_generator_files_path}/{original_name}", f"{project_final_path}/{new_name}")
            continue

        if os.path.isdir(f"{template_generator_files_path}/{file}"):
            shutil.copytree(f"{template_generator_files_path}/{file}", f"{project_final_path}/{file}")
        else:
            shutil.copy(f"{template_generator_files_path}/{file}", f"{project_final_path}/{file}")

    if rem_files:
        renamed_files = [file[0] for file in add_files if isinstance(file, tuple)]
        rem_files.extend(renamed_files)

        print("Excluding unnecessary folders and files.")
        for ex_file in rem_files:
            if os.path.isdir(f"{project_final_path}/{ex_file}"):
                attempt = 0
                try:
                    shutil.rmtree(f"{project_final_path}/{ex_file}")
                except PermissionError:
                    if attempt >= 3:
                        raise PermissionError(f"Could not delete folder: {ex_file}")
                    else:
                        attempt += 1
                        time.sleep(2)

            else:
                os.remove(f"{project_final_path}\\{ex_file}")