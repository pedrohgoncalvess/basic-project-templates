import zipfile
import io
import os
import shutil

import requests


def download_gh_repo(repo_owner:str, repo_name:str, destination_path:str, branch:str) -> None:
    """
    This function downloads a repository as a ZIP file from GitHub, extracts it,
    and places the contents in the specified destination directory.

    Parameters:
        repo_owner (str): The GitHub username or organization that owns the repository.
        repo_name (str): The name of the repository to download.
        destination_path (str): The local directory path where the repository contents will be placed.
        branch (str, optional): The branch to download. Defaults to "main".

    Raises:
        requests.exceptions.RequestException: If there's an error downloading the repository.
        zipfile.BadZipFile: If the downloaded content is not a valid ZIP file.
        OSError: If there are file system errors during extraction or copying.
    """

    zip_url = f"https://github.com/{repo_owner}/{repo_name}/archive/refs/heads/{branch}.zip"

    print(f"Downloading FastAPI template...")
    response = requests.get(zip_url)
    response.raise_for_status()

    os.makedirs(destination_path, exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        temp_dir = os.path.join(destination_path, "temp_extract")
        os.makedirs(temp_dir, exist_ok=True)
        zip_ref.extractall(temp_dir)

        extracted_dir = os.path.join(temp_dir, f"{repo_name}-{branch}")

        for item in os.listdir(extracted_dir):
            s = os.path.join(extracted_dir, item)
            d = os.path.join(destination_path, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

        shutil.rmtree(temp_dir)