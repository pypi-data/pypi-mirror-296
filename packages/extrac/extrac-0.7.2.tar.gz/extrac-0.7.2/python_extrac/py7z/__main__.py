import sys

from python_extrac.py7z import unpack_7z
from python_extrac.utils import confirm_out


def main(argv: list[str]):
    if len(argv) == 1 or argv[1] in ("-h", "--help"):
        print(
            "usage: python -m python_extrac.py7z <filename>.7z "
            "or python -m python_extrac.py7z <filename>.7z <to_directory>"
        )
        sys.exit(0)

    filepath, output = confirm_out(argv[0], argv[1])

    unpack_7z(filepath, output)


if __name__ == "__main__":
    main(sys.argv[1:])
