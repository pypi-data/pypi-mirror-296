from pathlib import Path

import zstandard as zstd


def unpack_zstd(file_path, output_path, chunk_size=1024 * 1024):
    output = Path(output_path)
    if output.is_dir():
        output_path = str(output / output.name)
    # Open the zstd compressed file
    with open(file_path, "rb") as f:
        dctx = zstd.ZstdDecompressor()
        with dctx.stream_reader(f) as reader, open(output_path, "wb") as writer:
            while True:
                data = reader.read(chunk_size)
                if not data:
                    break
                writer.write(data)
