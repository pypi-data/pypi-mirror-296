from pathlib import Path

import click
from bs4 import BeautifulSoup
from pytempl import render

from .loader import load_build_function_instance


def _update_paths_in_soup(
    soup: BeautifulSoup,
    build_output_dir: Path,
    build_static_css_dir: Path,
    build_static_js_dir: Path,
    build_static_assets_dir: Path,
    prefix: str,
    debug: bool = False,
) -> BeautifulSoup:
    if debug:
        click.echo("Updating paths in HTML...")
    # Update link, img, script & a tags
    for tag_name, attribute in [
        ("link", "href"),
        ("img", "src"),
        ("script", "src"),
        ("a", "href"),
    ]:
        for tag in soup.find_all(tag_name):
            if attribute in tag.attrs:
                if not tag[attribute].startswith(("http://", "https://", "/")):
                    old_path = Path(tag[attribute])
                    if Path("styles") in old_path.parents:
                        new_path = build_static_css_dir / old_path.relative_to("styles")
                    elif Path("js_scripts") in old_path.parents:
                        new_path = build_static_js_dir / old_path.relative_to(
                            "js_scripts"
                        )
                    elif Path("assets") in old_path.parents:
                        new_path = build_static_assets_dir / old_path.relative_to(
                            "assets"
                        )
                    elif Path("public") in old_path.parents:
                        new_path = build_output_dir / old_path.relative_to("public")
                    else:
                        # Note: Need to find a better way to handle pages condition. Right now, we are just shoving it in this else block.
                        # Note: Assuming the stem in href is same as the page_name mentioned in the config.
                        if ".html" in old_path.name:
                            new_path = build_output_dir / old_path.relative_to(".")
                        else:
                            new_path = build_output_dir / old_path.name

                    new_path = new_path.relative_to(build_output_dir)
                    if prefix:
                        new_path = prefix / new_path

                    if debug:
                        click.echo(f"Updating {attribute}: {old_path} -> /{new_path}")
                    tag[attribute] = f"/{new_path}"

    return soup


def builder(
    output_html_file_name: str,
    file_target: Path,
    function_target: str,
    build_output_dir: Path,
    build_static_css_dir: Path,
    build_static_js_dir: Path,
    build_static_assets_dir: Path,
    prefix: str,
    debug: bool = False,
) -> None:
    if debug:
        click.echo(
            f"Loading build function instance for '{output_html_file_name}.html'..."
        )
    instance = load_build_function_instance(file_target, function_target)

    if debug:
        click.echo("Rendering HTML...")
    rendered_html = render(instance())
    soup = BeautifulSoup(rendered_html, "html.parser")
    updated_soup = _update_paths_in_soup(
        soup=soup,
        build_output_dir=build_output_dir,
        build_static_css_dir=build_static_css_dir,
        build_static_js_dir=build_static_js_dir,
        build_static_assets_dir=build_static_assets_dir,
        prefix=prefix,
        debug=debug,
    )

    output_html_path = build_output_dir / output_html_file_name
    if not output_html_path.parent.exists():
        if debug:
            click.echo(f"Creating routing directory: {output_html_path.parent}")
        output_html_path.parent.mkdir(parents=True)

    if debug:
        click.echo("Writing final HTML to file...")
    with open(output_html_path, "w", encoding="utf-8") as file:
        file.write(updated_soup.decode(pretty_print=True, formatter="html5"))
