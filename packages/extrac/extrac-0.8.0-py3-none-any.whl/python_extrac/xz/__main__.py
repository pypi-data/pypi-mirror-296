from python_extrac.args import make_argparser
from python_extrac.utils import confirm_out
from python_extrac.xz import unpack_xz


def main():
    parser = make_argparser("python_extrac.xz")
    args = parser.parse_args()
    filepath, output = confirm_out(args.filepath, args.output)

    unpack_xz(file_path=filepath, output_path=output, encoding=args.encoding)


if __name__ == "__main__":
    main()
