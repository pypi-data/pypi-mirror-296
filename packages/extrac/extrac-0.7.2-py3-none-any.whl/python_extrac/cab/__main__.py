import sys

from python_extrac.cab import unpack_cab
from python_extrac.utils import confirm_out


def main(argv):
    if len(argv) == 1 or argv[1] in ("-h", "--help"):
        print(
            "usage: python -m python_extrac.cab <filename>.cab "
            "or python -m python_extrac.cab <filename>.cab <to_directory>"
        )
        sys.exit(0)

    filepath, output = confirm_out(argv[0], argv[1])

    unpack_cab(file_path=filepath, output_folder=output)


if __name__ == "__main__":
    main(sys.argv[1:])
