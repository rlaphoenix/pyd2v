from pathlib import Path
from typing import Optional

import jsonpickle

from pyd2v import D2V
import click


@click.command(context_settings=dict(
    help_option_names=["-?", "-h", "--help"],
    max_content_width=116,  # max PEP8 line-width, -4 to adjust for initial indent
))
@click.argument("file", type=Path)
@click.argument("key", type=str, required=False)
@click.option("-j", "--json", is_flag=True, default=False,
              help="Return D2V data as a JSON object.")
@click.option("-p", "--pretty", is_flag=True, default=False,
              help="Return D2V data as a prettified object.")
def main(file: Path, key: Optional[str], json: bool, pretty: bool):
    """
    \b
    Access a D2V file via CLI.
    For more information see the project at: https://github.com/rlaphoenix/pyd2v
    Copyright (c) 2020-2023 rlaphoenix — MIT License

    \b
    [FILE] is the path to a D2V object you wish to parse.
    [KEY] is an optional object-path you may wish to use to access data from the D2V.
          e.g. `settings.Aspect_Ratio` will get you the Aspect Ratio.
    """
    if not isinstance(file, Path) or not file:
        raise click.BadParameter("File is an invalid value. Must be a pathlib.Path object.", param_hint="file")
    if not file.exists():
        raise click.BadParameter("File path does not exist.", param_hint="file")
    if not file.is_file():
        raise click.BadParameter("File path is to a directory, not a file.", param_hint="file")
    d2v = D2V.load(file)
    if key:
        for path in key.split("."):
            if isinstance(d2v, dict):
                d2v = d2v[path]
            else:
                d2v = getattr(d2v, path)
    if json:
        print(jsonpickle.encode(
            d2v,
            unpicklable=True,
            indent=2 if pretty else None,
            separators=(",", ": ") if pretty else None
        ))
        return
    print(d2v)
