"""Copy the pre-rendered front-page image to the output directory.

The entry image (entry.png) sits next to this script. This program copies
it to the output location the harness expects, so the entry runs on a bare
Python 3.13 interpreter with only the standard library available.

The output directory comes from MAKEFUN_OUTPUT_DIR when that variable is
set to a non-empty value; an empty value falls back to /output, which is
also the default when the variable is unset entirely.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, destination)
    print("Wrote entry image to " + destination)


if __name__ == "__main__":
    main()
