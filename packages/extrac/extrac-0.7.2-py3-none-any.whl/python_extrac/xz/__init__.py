import lzma


def unpack_xz(file_path: str, output_path: str, chunk_size: int = 1024 * 1024) -> None:
    with lzma.open(file_path, "rb") as f_in, open(output_path, "wb") as f_out:
        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                break
            f_out.write(chunk)
