import sys

from python_extrac.gz import unpack_gzip
from python_extrac.utils import confirm_out


def main(argv: list[str]):
    if len(argv) == 1 or argv[1] in ("-h", "--help"):
        print(
            "usage: python -m python_extrac.gz <filename>.gz "
            "or python -m python_extrac.gz <filename>.gz <to_directory>"
        )
        sys.exit(0)
    filepath, output = confirm_out(argv[0], argv[1])
    unpack_gzip(file_path=filepath, output_path=output)


if __name__ == "__main__":
    main(sys.argv[1:])
