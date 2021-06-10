from pathlib import Path

import jsonpickle

from pyd2v import D2V
import click


@click.command(context_settings=dict(
    help_option_names=["-?", "-h", "--help"],
    max_content_width=116,  # max PEP8 line-width, -4 to adjust for initial indent
))
@click.argument("file", type=Path)
@click.option("-j", "--json", is_flag=True, default=False,
              help="Return D2V data as a JSON object.")
@click.option("-p", "--pretty", is_flag=True, default=False,
              help="Return D2V data as a prettified object.")
def main(file: Path, json: bool, pretty: bool):
    if not isinstance(file, Path) or not file:
        raise click.BadParameter("File is an invalid value. Must be a pathlib.Path object.", param_hint="file")
    if not file.exists():
        raise click.BadParameter("File path does not exist.", param_hint="file")
    if not file.is_file():
        raise click.BadParameter("File path is to a directory, not a file.", param_hint="file")
    d2v = D2V(str(file))
    if json:
        print(jsonpickle.encode(
            d2v,
            unpicklable=True,
            indent=2 if pretty else None,
            separators=(",", ": ") if pretty else None
        ))
        return
    print(d2v)
