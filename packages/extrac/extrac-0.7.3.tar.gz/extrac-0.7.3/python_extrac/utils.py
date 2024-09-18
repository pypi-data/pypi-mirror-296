#!/usr/bin/env python
#
# @author [belingud]
# @email [zyx@lte.ink]
# @create date 2019-11-11
# @desc [one command to unpack archives]

import shutil
import sys
import tarfile
from collections import OrderedDict
from pathlib import Path
from subprocess import CompletedProcess, run
from typing import Callable, Optional, Union

import click
import filetype
from click.exceptions import Exit
from filetype import Type

defenc = sys.getdefaultencoding()

_PYTHON = sys.executable

_UNPACK_TAR = [_PYTHON, "-W", "ignore", "-m", "tarfile", "-e"]
_UNPACK_ZSTD = [_PYTHON, "-m", "python_extrac.zstd"]
_EXTRACT_CMD: OrderedDict[str, list] = OrderedDict(
    {
        "rar": [_PYTHON, "-m", "rarfile", "-e"],
        "zip": [_PYTHON, "-m", "zipfile", "-e"],
        "tar.gz": _UNPACK_TAR,  # tar.gz should ahead of gz
        "tar.bz2": _UNPACK_TAR,  # tar.bz2 should ahead of bz2
        "tar.bz": _UNPACK_TAR,  # tar.bz should ahead of bz
        "tar.xz": _UNPACK_TAR,  # tar.xz should ahead of xz
        "tgz": _UNPACK_TAR,
        "gz": [_PYTHON, "-m", "python_extrac.gz"],
        "Z": [_PYTHON, "-m", "python_extrac.unlzw"],
        "bz2": [_PYTHON, "-m", "python_extrac.bz2"],
        "bz": [_PYTHON, "-m", "python_extrac.bz2"],
        "txz": _UNPACK_TAR,
        "xz": [_PYTHON, "-m", "python_extrac.xz"],
        "cab": [_PYTHON, "-m", "python_extrac.cab"],
        "ar": [_PYTHON, "-m", "python_extrac.ar"],
        "7z": [_PYTHON, "-m", "python_extrac.py7z"],
        "tar": _UNPACK_TAR,
        "deb": [_PYTHON, "-m", "python_extrac.deb"],
        "zstd": _UNPACK_ZSTD,
        "zst": _UNPACK_ZSTD,
        "cbr": [_PYTHON, "-m", "rarfile", "-e"],
    }
)

_ZIP_LIST = _EXTRACT_CMD.keys()

_TAR_MODE = {
    "tar.gz": "r:gz",
    "tar.bz2": "r:bz2",
    "tar.bz": "r:bz2",
    "tar.xz": "r:xz",
    "tbz2": "r:bz2",
    "tbz": "r:bz2",
    "tgz": "r:gz",
    "txz": "r:xz",
}


def confirm_out(filepath: Union[str, Path], output: Optional[Union[str, Path]] = None) -> tuple[str, str]:
    """
    get output path, if output is None, will use current directory
    :return:
    """
    path = Path(filepath)
    if not path.is_file():
        click.echo(f'"{filepath}" is not a file')
        raise Exit(1)
    if not output:
        file_format = get_file_format(filepath)
        output = Path.cwd() / path.name[: -len(file_format) - 1]
        output.mkdir(parents=True, exist_ok=True)
        output = output.relative_to(Path.cwd())
    if not Path(output).is_dir():
        raise FileNotFoundError(f'"{output}" is not a directory')
    return str(filepath), str(output)


def get_tarfile_mode(file_path: str) -> str:
    """
    get tarfile read mode
    :return: read mode
    """
    if not isinstance(file_path, str):
        file_path = str(file_path)
    for k, v in _TAR_MODE.items():
        if file_path.endswith(k):
            return v
    return "r"


def make_sure_extension(guess_ext: str, filepath: str) -> str:
    """
    Some file name is not ends with file type exactly
    :param guess_ext:
    :param filepath:
    :return:
    """
    if guess_ext == "bz2" and filepath.endswith("bz"):
        return "bz"
    return guess_ext


def get_file_format(filepath: str) -> Optional[str]:
    """
    judge the file type, return of suffix of the file
    :param filepath:
    :return:
    """
    guess: Type = filetype.guess(filepath)
    if not guess:
        # click.echo(f"Error: unknown file type `{filepath}`")
        return
    guess_ext: str = make_sure_extension(guess.extension, filepath=filepath)
    for ext in _ZIP_LIST:
        if filepath.endswith(".a") and guess_ext == "ar":
            extension = "a"
            break
        if filepath.endswith(ext) and guess_ext in ext:
            extension = ext
            break
    else:
        extension = guess.extension
    return extension


def call(command: list[str], **kwargs) -> CompletedProcess:
    """
    call shell command
    :param command: format the command before call this method
    :return:
    """

    return run(command, text=True, **kwargs)


def extract_to(file: str, work_dir: str, extension: str = None) -> str:
    """
    Gen extract directory by file type in work_dir
    """
    f = Path(file)
    if not extension:
        extension = get_file_format(file)
    output = Path(work_dir) / f.name[: -len(extension) - 1]
    return str(output)


def extract_archive(file_path: str, output: str = None, file_format: str = None) -> None:
    """
    :param file_path:
    :param output:
    :param file_format:
    :return:
    """
    file_format = file_format or get_file_format(file_path)
    if file_format == "a":
        # .a files are the same with .ar files
        file_format = "ar"
    cmd = _EXTRACT_CMD[file_format]
    cmd.append(file_path)
    if output:
        cmd.append(output)
    call(cmd)


def open_and_extract(
    filepath: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    extension: str = None,
    _open: Callable = open,
):
    """
    Extract gz/bz2/xz archive
    Args:
        filepath: Union[str, Path]
        output_path: output path
        extension: str file extension
        _open: Callable open function
    """
    assert output_path or extension, "output_path or extension must be provided"
    filepath = Path(filepath)
    unpack_dir = Path(output_path or str(filepath)[: -len(extension)])
    with _open(filepath, "rb") as f_in:
        unpack_filename = filepath.stem
        # unpack to same filename directory
        Path(unpack_dir).mkdir(parents=True, exist_ok=True)
        # create empty file, same name without extension
        unpack_fullpath = unpack_dir / unpack_filename
        # unpack file to unpack_path
        with open(unpack_fullpath, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    # guess filetype by unpacked file bytes
    guess = filetype.guess(unpack_fullpath)
    if guess:
        extension = guess.extension
        if extension not in unpack_filename:
            rename_path = str(unpack_fullpath) + "." + extension
            # rename unpacked file by guessed extension
            shutil.move(unpack_fullpath, rename_path)
            click.echo(
                f"guess unpacked file format: {extension}, "
                f"renamed {unpack_fullpath.name} to {unpack_fullpath.name}.{extension}"
            )
