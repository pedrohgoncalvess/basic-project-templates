import os
import shutil
import time


def _substitute_in_file(file_path: str, project_name: str) -> None:
    """Replace $$project_name$$ placeholder inside a copied text file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, OSError):
        # Binary or unreadable file: leave it untouched.
        return

    if "$$project_name$$" not in content:
        return

    content = content.replace("$$project_name$$", project_name)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def _substitute_in_dir(dir_path: str, project_name: str) -> None:
    """Replace $$project_name$$ placeholder in every file under a directory."""
    for root, _dirs, files in os.walk(dir_path):
        for name in files:
            _substitute_in_file(os.path.join(root, name), project_name)


def copy_project_files(project_final_path: str, npt_files_path: str, add_files: list[tuple[str] | str], rem_files: list[str], project_name: str | None = None):
    for file in add_files:
        os.makedirs(project_final_path, exist_ok=True)
        if isinstance(file, tuple):
            original_name = file[0]
            new_name = file[1]
            src = f"{npt_files_path}/{original_name}"

            if os.path.isdir(src):
                dest = f"{project_final_path}/{new_name}"
                shutil.copytree(src, dest)
                if project_name:
                    _substitute_in_dir(dest, project_name)
            else:
                dest = f"{project_final_path}/{new_name}"
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy(src, dest)
                if project_name:
                    _substitute_in_file(dest, project_name)
            continue

        src = f"{npt_files_path}/{file}"
        if os.path.isdir(src):
            dest = f"{project_final_path}/{file}"
            shutil.copytree(src, dest)
            if project_name:
                _substitute_in_dir(dest, project_name)
        else:
            dest = f"{project_final_path}/{file}"
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy(src, dest)
            if project_name:
                _substitute_in_file(dest, project_name)

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