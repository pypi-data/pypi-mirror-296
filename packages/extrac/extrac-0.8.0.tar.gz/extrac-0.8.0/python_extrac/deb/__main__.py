import sys

from python_extrac.deb import unpack_deb
from python_extrac.utils import confirm_out


def main(argv: list[str]):
    if len(argv) == 1 or argv[1] in ("-h", "--help"):
        print(
            "usage: python -m python_extrac.deb <filename>.deb "
            "or python -m python_extrac.deb <filename>.deb <to_directory>"
        )
        sys.exit(0)
    filepath, output = confirm_out(argv[0], argv[1])
    unpack_deb(deb_file=filepath, extract_to=output)


if __name__ == "__main__":
    main(sys.argv[1:])
