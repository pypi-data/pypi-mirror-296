import os
from pathlib import Path
from typing import Union, cast

import arpy


def unpack_ar(
    file_path: Union[str, Path],
    output_path: Union[str, Path],
    buffer_size: int = 1024 * 1024,
):
    """
    Extract ar archive to output_path directory
    """
    with arpy.Archive(str(file_path)) as archive:
        archive.read_all_headers()
        for member in archive.archived_files:
            member = cast(bytes, member)
            member_path = os.path.join(output_path, member.decode())
            # Make sure inside directory exists
            Path(member_path).parent.mkdir(parents=True, exist_ok=True)
            os.path.exists(output_path) or os.makedirs(output_path, exist_ok=True)
            # support big files
            with open(member_path, "wb") as f:
                while True:
                    chunk = archive.archived_files[member].read(buffer_size)
                    if not chunk:
                        break
                    f.write(chunk)
