import argparse
import sys
from pathlib import Path

from python_extrac.unlzw.unpack import unlzw_chunked


def main() -> None:
    parser = argparse.ArgumentParser("python_extrac.unlzw")
    parser.add_argument('filepath', help='archive file path')
    parser.add_argument('output', nargs="?", help='output file path')
    args = parser.parse_args()
    filepath = Path(args.filepath)
    to = args.output or None
    if not to:
        to = filepath.parent / filepath.stem
        to.mkdir(parents=True, exist_ok=True)
    unpack_filepath = Path(to) / filepath.stem
    with open(args[0], "rb") as f_z, open(unpack_filepath, "wb") as f_out:
        for chunk in unlzw_chunked(f_z):
            f_out.write(chunk)


if __name__ == "__main__":
    main()
