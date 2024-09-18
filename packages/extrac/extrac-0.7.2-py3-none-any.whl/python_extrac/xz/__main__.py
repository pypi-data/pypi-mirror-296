import sys

from python_extrac.utils import confirm_out
from python_extrac.xz import unpack_xz


def main(argv: list[str]):
    if len(argv) == 1 or argv[1] in ("-h", "--help"):
        print(
            "usage: python -m python_extrac.xz <filename>.xz or python -m python_extrac.xz <filename>.xz <to_directory>"
        )
        sys.exit(0)
    filepath, output = confirm_out(argv[0], argv[1])

    unpack_xz(file_path=filepath, output_path=output)
