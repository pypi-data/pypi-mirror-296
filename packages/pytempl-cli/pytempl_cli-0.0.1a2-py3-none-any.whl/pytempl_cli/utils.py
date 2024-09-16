import ast
import shutil
import warnings
from pathlib import Path
from typing import List
from urllib.request import Request, urlopen

import click


def create_dir_if_not_exists(directory: Path, debug: bool = False) -> None:
    if not directory.exists():
        if debug:
            click.echo(f"Creating directory: {directory}")
        directory.mkdir(parents=True)


def create_file_if_not_exists(file: Path, debug: bool = False) -> None:
    if not file.exists():
        if debug:
            click.echo(f"Creating empty file: {file}")
        file.touch()


def copy_dir(src: Path, dest: Path, directory_name: str, debug: bool = False) -> None:
    if src and src.exists():
        if debug:
            click.echo(f"Copying {directory_name} from {src} to {dest}")
        shutil.copytree(src, dest, dirs_exist_ok=True)
    else:
        warnings.warn(
            f"Project doesn't have a '{src}' directory.",
            UserWarning,
            stacklevel=1,
        )


def get_dependent_components(component_file_content: str) -> List[str]:
    tree = ast.parse(component_file_content)
    dependent_components = [
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        if node.level > 0
    ]
    return dependent_components


def resolve_component_dependencies(
    component_dir: Path, component_list: List[str], debug: bool = False
) -> None:
    for component_name in component_list:
        component_path = component_dir / f"{component_name}.py"
        if component_path.exists():
            with open(component_path) as file:
                component_file_content = file.read()
        else:
            if debug:
                click.echo(f"Component '{component_name}' not found. Downloading it...")
            request = Request(
                f"https://raw.githubusercontent.com/pytempl/ui/main/src/ui/{component_name}.py"
            )
            component_file_content = urlopen(request).read().decode("utf-8")
            with open(component_path, "w") as file:
                file.write(component_file_content)

        dependent_components = get_dependent_components(component_file_content)
        if dependent_components:
            resolve_component_dependencies(component_dir, dependent_components)
