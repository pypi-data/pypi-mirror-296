import lzma
from pathlib import Path


def unpack_xz(
    file_path: str,
    output_path: str,
    encoding: str = "utf-8",
    chunk_size: int = 1024 * 1024,
) -> None:
    """
    Extract xz archive
    """
    if not encoding:
        raise ValueError("encoding must not be empty")
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if not isinstance(encoding, str):
        raise TypeError("encoding must be a string")
    if not isinstance(chunk_size, int):
        raise TypeError("chunk_size must be an integer")
    o = Path(output_path)
    if o.is_dir():
        output_path = str(o / o.name)
    with lzma.open(file_path, "rt", encoding=encoding) as f_in, open(
        output_path, "w", encoding=encoding
    ) as f_out:
        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                break
            f_out.write(chunk)
