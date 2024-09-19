import argparse

from python_extrac.utils import confirm_out
from python_extrac.zstd import unpack_zstd


def main():
    parser = argparse.ArgumentParser("python_extrac.zstd")
    parser.add_argument('filepath', help='archive file path')
    parser.add_argument('output', nargs="?", help='output file path')
    args = parser.parse_args()
    filepath, output = confirm_out(args.filepath, args.output)
    unpack_zstd(file_path=filepath, output_path=output)


if __name__ == "__main__":
    main()
