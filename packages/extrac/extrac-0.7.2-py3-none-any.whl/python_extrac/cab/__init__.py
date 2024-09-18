import os
from pathlib import Path

import cabarchive
from cabarchive import CabFile, CorruptionError, NotSupportedError


def unpack_cab(file_path, output_folder) -> None:
    """
    extract files from cab archive
    :param file_path: the path of cab file
    :param output_folder: the path of output folder
    """
    os.path.exists(output_folder) or os.makedirs(output_folder)

    with open(file_path, "rb") as f:
        try:
            archive = cabarchive.CabArchive(f.read())
        except NotSupportedError as not_support:
            # some archive is not supported like LZX or Chained cab file,and some version not supported
            print(f"NotSupportedError: {not_support}")
            return
        except CorruptionError as corruption:
            print(f"CorruptionError: {corruption}")
            return
        for filename in archive:
            cff: CabFile = archive[filename]
            filename: str = filename.replace("\\", "/")
            output_path: str = os.path.join(output_folder, filename)
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as out_file:
                out_file.write(cff.buf)
