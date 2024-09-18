#!/usr/bin/env python
#
# @author [belingud]
# @email [zyx@lte.ink]
# @create date 2019-11-11
# @desc [one command to unpack archives]

import os
from pathlib import Path
from typing import cast

import click
from click import Argument, Context

from python_extrac.utils import extract_archive, extract_to, get_file_format

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])

help_string = """This is a magic command line tool to extract archives,
only use one command "x FILE", enjoy it.\n
Support 7z(.7z),AR(.a,.ar),RAR(.rar),ZIP(.zip,.jar),TAR(.tar.gz,.tgz,.tar.bz,.tar.bz2,.tbz,.tbz2,.tar.xz,.txz),\
GZIP(.gz),compress(.Z),CAB(.cab),XZ(.xz,.lzma),BZIP2(.bz2,.dmg),BZIP(.bz),ZSTD(.zstd,.zst),DEB(deb) archives.\n
Will extract to current directory if not specified by -o."""


def check_arguments(
    ctx: Context, param: Argument, value: tuple[...]
) -> tuple[...]:  # noqa
    """
    check if FILE argument is empty
    """
    if not value:
        click.echo(ctx.get_help())
        ctx.exit()
    return value


@click.command(context_settings=CONTEXT_SETTINGS, help=help_string)
@click.argument(
    "files",
    type=click.Path(exists=True),
    default=None,
    nargs=-1,
    callback=check_arguments,
)
@click.option(
    "-o",
    "--output",
    "work_dir",
    type=click.Path(),
    default=None,
    help="output directory",
)
@click.option(
    "-r",
    "--remove",
    default=0,
    type=click.INT,
    help="remove the archive after extrac",
    is_flag=True,
    required=False,
)
def cli(files, work_dir, remove):
    """One command line tool to extract archives."""
    if not work_dir:
        work_dir: str = os.getcwd()
    for file in files:
        file: cast(str, files)
        file_format = get_file_format(file)
        if not file_format:
            click.echo(f"Error: unknown file type `{file}`")
            continue
        extract_dir = extract_to(file=file, work_dir=work_dir, extension=file_format)
        dir_path_obj = Path(extract_dir)
        dir_path_obj.mkdir(parents=True, exist_ok=True)
        try:
            _r_path = dir_path_obj.relative_to(Path.cwd())
        except ValueError:
            _r_path = dir_path_obj
        click.echo(f"extracting {file} to {_r_path}")
        extract_archive(file_path=file, output=extract_dir, file_format=file_format)
    if remove:
        os.unlink(files)


if __name__ == "__main__":
    cli()
