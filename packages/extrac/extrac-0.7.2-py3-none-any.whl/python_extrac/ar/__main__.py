import sys

from python_extrac.ar import unpack_ar
from python_extrac.utils import confirm_out


def main(argv: list[str]):
    if len(argv) == 1 or argv[1] in ("-h", "--help"):
        print(
            "usage: python -m python_extrac.ar <filename>.ar or python -m python_extrac.ar <filename>.ar <to_directory>"
        )
        sys.exit(0)
    filepath, output = confirm_out(argv[0], argv[1])

    unpack_ar(file_path=filepath, output_path=output)


if __name__ == "__main__":
    main(sys.argv[1:])
