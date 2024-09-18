import sys

from python_extrac.utils import confirm_out
from python_extrac.zstd import unpack_zstd


def main(argv: list[str]):
    if len(argv) == 1 or argv[1] in ("-h", "--help"):
        print(
            "usage: python -m python_extrac.zstd <filename>.zst "
            "or python -m python_extrac.zstd <filename>.zst <to_directory>"
        )
        sys.exit(0)
    filepath, output = confirm_out(argv[0], argv[1])
    unpack_zstd(file_path=filepath, output_path=output)


if __name__ == "__main__":
    main(sys.argv[1:])
