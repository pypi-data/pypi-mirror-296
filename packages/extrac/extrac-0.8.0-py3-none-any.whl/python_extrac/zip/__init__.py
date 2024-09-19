import zipfile


def unpack_zip(file: str, output: str, encoding: str = "utf-8") -> None:
    with zipfile.ZipFile(file, mode="r", metadata_encoding=encoding) as zf:
        for file in zf.infolist():
            if output:
                zf.extract(file, output)
            else:
                zf.extract(file)
