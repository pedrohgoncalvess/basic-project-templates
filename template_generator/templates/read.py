from typing import Tuple
import re

import yaml

from template_generator.utils import project_root


def get_template_items(template_name:str) -> list[str]:
    with open(f"{project_root}\\templates\\main.yaml", 'r') as file:
        data = yaml.safe_load(file)
        return data['templates'].get(template_name, [])

        
def get_possible_templates() -> list[str]:
    with open(f"{project_root}\\templates\\main.yaml", 'r') as file:
        data = yaml.safe_load(file)
        return data['templates'].keys()


def parse_template_items(items: list[str]) -> Tuple[str, any, any]:
    new_items = []
    rem_items = []
    pattern = r'f\(([^)]+)\)\s*>\s*((?:[^,]+(?:,\s*|$))+)'

    for item in items:
        match = re.match(pattern, item)
        if match:
            function_name = match.group(1).strip()
            args_string = match.group(2).strip()
            args = [arg.strip() for arg in args_string.split(',')]

            return "function", function_name, args

        if item.endswith("**"): #TODO: Refac this pattern
            command = item.replace("**", "")
            new_items.append(("command", command.split(" ")))
            continue

        if item.endswith("!"):
            rem_items.append(item.replace("!", ""))
            continue

        if item.__contains__(">>"):
            splt_file = item.split(">>")
            new_items.append({splt_file[0].strip():splt_file[1].strip()})
            continue

        new_items.append(item)

    return "normal", new_items, rem_items
