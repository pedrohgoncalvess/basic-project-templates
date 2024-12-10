import argparse
import os


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Python projects with template.")
    parser.add_argument("--name", type=str, required=True)
    parser.add_argument("--path", type=str, default=".",
                        help="Path to create project.")
    parser.add_argument("--template", type=str, required=False,
                        help="Template to use.")

    args = parser.parse_args()

    project_name = args.name
    project_path = os.path.abspath(args.path)

    print(project_path, project_name)


main()