from typing import Tuple
import re

import yaml

from npt.utils import project_root


def _load_templates() -> dict:
    with open(f"{project_root}\\templates\\main.yaml", 'r') as file:
        return yaml.safe_load(file)['templates']


def get_template_items(template_name: str) -> list[str]:
    templates = _load_templates()
    template = templates.get(template_name, {})
    return template.get("files", [])


def get_possible_templates() -> list[str]:
    return list(_load_templates().keys())


def get_templates_info() -> dict[str, str]:
    """Return a mapping of template names to their descriptions."""
    return {
        name: info.get("description", "No description available.")
        for name, info in _load_templates().items()
    }


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
            new_items.append((splt_file[0].strip(), splt_file[1].strip()))
            continue

        new_items.append(item)

    return "normal", new_items, rem_items
