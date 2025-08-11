import base64
import lzma


def fix_padding(b64_string):
    return b64_string + "=" * ((4 - len(b64_string) % 4) % 4)


def read_lzma_point_cloud(filename):
    with open(filename, "r") as file:
        compressed_b64 = file.read().strip()

    compressed_bytes = base64.b64decode(fix_padding(compressed_b64))
    decompressed_bytes = lzma.decompress(compressed_bytes)
    decompressed_str = decompressed_bytes.decode()

    lines = decompressed_str.splitlines()
    points = []
    v, t = None, None

    for line in lines[:-3]:  # First lines are points
        if line.strip():
            x, y, z = map(float, line.split())
            points.append([x, y, z])  # Convert to list for Open3D

    last_lines = [line.strip() for line in lines[-3:] if line.strip()]
    if len(last_lines) >= 2:
        v = float(last_lines[-2])  # Velocity
        t = float(last_lines[-1])  # Time

    return points, v, t
