import sys
from pathlib import Path

from python_extrac.unlzw.unpack import unlzw_chunked


def main(args: list[str]) -> None:
    if not args or args[0] in ("-h", "--help"):
        print(
            "usage: python -m python_extrac.unlzw <filename>.Z "
            "or python -m python_extrac.unlzw <filename>.Z <to_directory>"
        )
        return
    file = args[0]
    filepath = Path(file)
    to = args[1] if len(args) > 1 else None
    if not to:
        to = filepath.parent / filepath.stem
        to.mkdir(parents=True, exist_ok=True)
    unpack_filepath = Path(to) / filepath.stem
    with open(args[0], "rb") as f_z, open(unpack_filepath, "wb") as f_out:
        for chunk in unlzw_chunked(f_z):
            f_out.write(chunk)


if __name__ == "__main__":
    main(sys.argv[1:])
