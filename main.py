"""World news image entry for Sunday 22 November 2026.

Copies the finished front page, entry.png, to the output path the
harness asks for (/output/entry.png when graded, ./out/entry.png
locally). Standard library only, no network, deterministic: the same
input file always produces the same output bytes.

The picture itself was drawn by build_image.py in this same
repository (Pillow, run once by the agent while building the entry);
this program is only the delivery step, so it runs anywhere.
"""
import hashlib
import os
import shutil
import sys

NAME = "entry.png"
MAX_BYTES = 1_048_576


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, NAME)
    if not os.path.isfile(src):
        print(f"missing {NAME} next to main.py", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, NAME)
    shutil.copyfile(src, dst)

    size = os.path.getsize(dst)
    if size > MAX_BYTES:
        print(f"{NAME} is {size} bytes, over the 1 MiB limit",
              file=sys.stderr)
        return 1
    with open(dst, "rb") as fh:
        head = fh.read(8)
    if head != b"\x89PNG\r\n\x1a\n":
        print(f"{NAME} is not a PNG (bad signature)", file=sys.stderr)
        return 1
    digest = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    print(f"wrote {dst} ({size} bytes, sha256 {digest[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
