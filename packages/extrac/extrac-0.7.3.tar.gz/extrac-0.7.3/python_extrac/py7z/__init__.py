import py7zr


def unpack_7z(file_path, output_path):
    with py7zr.SevenZipFile(file_path, mode="r") as archive:
        archive.extractall(output_path)
