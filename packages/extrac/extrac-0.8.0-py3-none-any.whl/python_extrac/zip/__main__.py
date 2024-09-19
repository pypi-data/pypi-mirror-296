import sys

from python_extrac.args import make_argparser
from python_extrac.utils import confirm_out
from python_extrac.zip import unpack_zip


def main():
    parser = make_argparser("python_extrac.zip")
    args = parser.parse_args()
    filepath, output = confirm_out(args.filepath, args.output)
    unpack_zip(filepath, output, args.encoding)


if __name__ == "__main__":
    main()
