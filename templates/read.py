from typing import Tuple

import yaml

from utils.path_config import project_root


def get_template_items(template_name:str) -> list[str]:
    with open(f"{project_root}\\templates\\main.yaml", 'r') as file:
        data = yaml.safe_load(file)
        return data['templates'].get(template_name, [])

def parse_template_items(items: list[str]) -> Tuple[list, list]:
    new_items = []
    rem_items = []
    for item in items:
        if item.endswith("!"):
            rem_items.append(item.replace("!", ""))
            continue

        if item.__contains__(">>"):
            splt_file = item.split(">>")
            new_items.append({splt_file[0].strip():splt_file[1].strip()})
            continue

        new_items.append(item)

    return new_items, rem_items
