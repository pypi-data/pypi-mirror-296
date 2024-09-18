import os
import sys
import tarfile
from typing import cast

import arpy

from python_extrac.utils import get_file_format, get_tarfile_mode

defenc = sys.getdefaultencoding()


def unpack_deb(deb_file, extract_to):
    """
    Extract deb archive to extract_to directory, including sub-tar archives like control.tar.gz and data.tar.gz
    """
    os.path.exists(extract_to) or os.makedirs(extract_to)

    with arpy.Archive(deb_file) as archive:
        archive.read_all_headers()
        for name in archive.archived_files:
            name = cast(bytes, name)
            name_str: str = name.decode(defenc)
            file_path = os.path.join(extract_to, name_str)
            with open(file_path, "wb") as out_file:
                out_file.write(archive.archived_files[name].read())
            # extract data.tar.gz and control.tar.gz
            if tarfile.is_tarfile(file_path):
                ext = get_file_format(file_path)
                mode: str = get_tarfile_mode(name_str)
                sub_tar_dir: str = os.path.join(extract_to, name_str[: -len(ext) - 1])
                os.path.exists(sub_tar_dir) or os.makedirs(sub_tar_dir)
                with tarfile.open(file_path, mode=mode) as tar:
                    tar.extractall(path=sub_tar_dir)
