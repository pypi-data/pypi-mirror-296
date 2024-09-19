import gzip

from python_extrac.utils import open_and_extract


def unpack_gzip(file_path: str, output_path: str = None, *args) -> None:
    """
    Extract gz archive
    """

    open_and_extract(
        file_path, extension=".gz", _open=gzip.open, output_path=output_path
    )
