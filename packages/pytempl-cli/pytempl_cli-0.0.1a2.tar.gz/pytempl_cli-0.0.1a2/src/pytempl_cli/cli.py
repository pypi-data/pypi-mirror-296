import contextlib
import http.server
import socket
from typing import Tuple

import click

from . import __version__
from .build_process import builder
from .loader import load_configs
from .utils import (
    copy_dir,
    create_dir_if_not_exists,
    create_file_if_not_exists,
    resolve_component_dependencies,
)


@click.command()
@click.argument("components", nargs=-1, type=str)
@click.option("--debug", is_flag=True, help="Enable debug mode to echo steps.")
def add(components: Tuple[str], debug: bool) -> None:
    pytempl_config = load_configs()

    create_dir_if_not_exists(pytempl_config.components_dir, debug)

    parent_dir_init_file = pytempl_config.components_dir.parent / "__init__.py"
    create_file_if_not_exists(parent_dir_init_file, debug)

    components_dir_init_file = pytempl_config.components_dir / "__init__.py"
    create_file_if_not_exists(components_dir_init_file, debug)

    resolve_component_dependencies(pytempl_config.components_dir, components)

    click.echo(f"'{components}' added successfully.")


@click.command()
@click.option(
    "--prefix",
    type=str,
    default="",
    help="Inject 'base_path' prefix in the generated HTML file.",
)
@click.option("--debug", is_flag=True, help="Enable debug mode to echo steps.")
def build(prefix: str, debug: bool) -> None:
    pytempl_config = load_configs()

    create_dir_if_not_exists(pytempl_config.build_output_dir, debug)

    build_static_dir = pytempl_config.build_output_dir / "static"
    create_dir_if_not_exists(build_static_dir, debug)

    build_static_css_dir = build_static_dir / "css"
    create_dir_if_not_exists(build_static_css_dir, debug)

    build_static_js_dir = build_static_dir / "js"
    create_dir_if_not_exists(build_static_js_dir, debug)

    build_static_assets_dir = build_static_dir / "assets"
    create_dir_if_not_exists(build_static_assets_dir, debug)

    copy_dir(pytempl_config.styles_dir, build_static_css_dir, "styles", debug)
    copy_dir(pytempl_config.js_scripts_dir, build_static_js_dir, "js_scripts", debug)
    copy_dir(pytempl_config.assets_dir, build_static_assets_dir, "assets", debug)
    copy_dir(
        pytempl_config.public_dir, pytempl_config.build_output_dir, "public", debug
    )

    if debug:
        click.echo("Building Index HTML...")
    builder(
        output_html_file_name="index.html",
        file_target=pytempl_config.build_index_page_file_target,
        function_target=pytempl_config.build_index_page_function_target,
        build_output_dir=pytempl_config.build_output_dir,
        build_static_css_dir=build_static_css_dir,
        build_static_js_dir=build_static_js_dir,
        build_static_assets_dir=build_static_assets_dir,
        prefix=prefix,
        debug=debug,
    )

    if pytempl_config.build_pages_file_targets:
        if debug:
            click.echo("Building Pages...")
        for file_target, function_target, page_name in zip(
            pytempl_config.build_pages_file_targets,
            pytempl_config.build_pages_function_targets,
            pytempl_config.build_pages_names,
        ):
            builder(
                output_html_file_name=f"{page_name}.html",
                file_target=file_target,
                function_target=function_target,
                build_output_dir=pytempl_config.build_output_dir,
                build_static_css_dir=build_static_css_dir,
                build_static_js_dir=build_static_js_dir,
                build_static_assets_dir=build_static_assets_dir,
                prefix=prefix,
                debug=debug,
            )

    click.echo("Built successfully")


@click.command()
def run() -> None:
    pytempl_config = load_configs()

    if not pytempl_config.build_output_dir.exists():
        click.echo("Build directory not found. Please run 'pytempl-cli build' first.")
        return

    server_handler_class = http.server.CGIHTTPRequestHandler

    class DualStackServer(http.server.ThreadingHTTPServer):
        def server_bind(self):
            # suppress exception when protocol is IPv4
            with contextlib.suppress(Exception):
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

        def finish_request(self, request, client_address):
            self.RequestHandlerClass(
                request, client_address, self, directory=pytempl_config.build_output_dir
            )

    click.echo("Starting dev server (don't use this in production)...")
    click.echo("Press Ctrl+C to stop the server.")

    http.server.test(
        server_handler_class,
        DualStackServer,
        port=pytempl_config.run_port,
        bind=pytempl_config.run_host,
        protocol="HTTP/1.0",
    )


@click.command()
def version() -> None:
    click.echo(f"Pytempl CLI version {__version__}")
