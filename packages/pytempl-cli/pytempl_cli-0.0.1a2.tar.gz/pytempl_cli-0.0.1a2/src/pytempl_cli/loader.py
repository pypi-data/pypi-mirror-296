import importlib
import importlib.util
import sys
from pathlib import Path
from typing import Any, List, Self, Union

import tomli
from pydantic import BaseModel, model_validator


class ImportFromStringError(Exception):
    pass


def load_build_function_instance(file_target: str, function_target: str) -> Any:
    working_dir = Path.cwd()
    working_file = Path(file_target)

    if not working_file.exists():
        raise FileNotFoundError(f"File '{file_target}' not found.")

    module_path = working_dir / file_target
    module_name = Path(file_target).stem

    sys.path.append(str(working_dir))

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        raise ImportFromStringError(
            f"Could not import module from path '{module_path}'"
        )

    try:
        instance = getattr(module, function_target)
    except AttributeError:
        message = f'Attribute "{function_target}" not found in module "{module_name}".'
        raise ImportFromStringError(message)

    return instance


class PytemplConfig(BaseModel):
    # Configuration for 'build' command
    build_index_page_file_target: Path
    build_index_page_function_target: str
    build_output_dir: Path
    build_pages_file_targets: List[Path]
    build_pages_function_targets: List[str]
    build_pages_names: List[str]

    # Path configurations for different 'pytempl-cli' commands
    assets_dir: Union[Path, None]
    components_dir: Path
    js_scripts_dir: Union[Path, None]
    public_dir: Union[Path, None]
    styles_dir: Union[Path, None]

    # Configuration for 'run' command
    run_host: str
    run_port: int

    @model_validator(mode="after")
    def validate_attrs(self) -> Self:
        if len(self.build_pages_file_targets) != len(self.build_pages_function_targets):
            raise ValueError(
                "Each build_pages_file_target must have a corresponding build_pages_function_target."
            )
        if len(self.build_pages_file_targets) != len(self.build_pages_names):
            raise ValueError(
                "Each build_pages_file_target must have a corresponding build_pages_name."
            )

        return self


def load_configs() -> PytemplConfig:
    pyproject_file = Path("pyproject.toml")
    if not pyproject_file.exists():
        raise FileNotFoundError("Unable to locate configuration file.")

    with open(pyproject_file, "rb") as file:
        raw_pytempl_config: dict = tomli.load(file).get("tool", {}).get("pytempl", {})
        raw_pytempl_build_config: dict = raw_pytempl_config.get("build", {})
        raw_pytempl_run_config: dict = raw_pytempl_config.get("run", {})

    # Decompose raw configurations into required PytemplConfig
    assets_dir = raw_pytempl_config.get("assets_dir")
    components_dir = raw_pytempl_config.get("components_dir", "ui/components/")
    js_scripts_dir = raw_pytempl_config.get("js_scripts_dir")
    public_dir = raw_pytempl_config.get("public_dir")
    styles_dir = raw_pytempl_config.get("styles_dir")

    # Decompose raw build configurations into required PytemplConfig
    build_output_dir = raw_pytempl_build_config.get("output_dir", "build/")

    build_index_page: dict = raw_pytempl_build_config.get("index_page", {})
    build_index_page_file_target = build_index_page.get("file_target", "main.py")
    build_index_page_function_target = build_index_page.get("function_target", "main")

    # TODO: Add fallbacks/defaults if the lengths of file_targets and function_targets are different
    build_pages: dict = raw_pytempl_build_config.get("pages", {})
    build_pages_file_targets = build_pages.get("file_targets", [])
    build_pages_function_targets = build_pages.get("function_targets", [])
    build_pages_names = build_pages.get("names", [])

    # Decompose raw run configurations into required PytemplConfig
    run_host = raw_pytempl_run_config.get("host", "0.0.0.0")
    run_port = raw_pytempl_run_config.get("port", 8080)

    return PytemplConfig(
        build_index_page_file_target=build_index_page_file_target,
        build_index_page_function_target=build_index_page_function_target,
        build_output_dir=build_output_dir,
        build_pages_file_targets=build_pages_file_targets,
        build_pages_function_targets=build_pages_function_targets,
        build_pages_names=build_pages_names,
        assets_dir=assets_dir,
        components_dir=components_dir,
        js_scripts_dir=js_scripts_dir,
        public_dir=public_dir,
        styles_dir=styles_dir,
        run_host=run_host,
        run_port=run_port,
    )
