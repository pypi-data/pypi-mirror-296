import sys

from python_extrac.bz2 import unpack_bz2
from python_extrac.utils import confirm_out


def main(argv: list[str]):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(
            "usage: python -m python_extrac.bz2 <filename>.bz2 "
            "or python -m python_extrac.bz2 <filename>.bz2 <to_directory>"
        )
        sys.exit(0)
    filepath, output = confirm_out(argv[0], argv[1])
    unpack_bz2(file_path=filepath, output_path=output)


if __name__ == "__main__":
    main(sys.argv[1:])
