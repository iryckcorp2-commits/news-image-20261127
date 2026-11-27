"""Copy the pre-rendered front-page image to the output directory.

The image entry.png sits next to this script. This program copies it to
entry.png inside the output directory, which is MAKEFUN_OUTPUT_DIR when
that variable is set to a non-empty value, or /output otherwise. An
empty MAKEFUN_OUTPUT_DIR therefore falls back to /output as well.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
DESTINATION = os.path.join(OUTPUT_DIR, "entry.png")

os.makedirs(OUTPUT_DIR, exist_ok=True)
shutil.copyfile(SOURCE, DESTINATION)
print(f"Wrote {DESTINATION}")
