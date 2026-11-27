"""Copy the pre-rendered front-page image to the output directory.

The image (entry.png, next to this script) was rendered by the agent's own
program in an earlier build step. This entrypoint is stdlib-only so it runs
in the bare make.fun sandbox: it just copies the file, byte for byte.
"""

import os
import shutil

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
DST = os.path.join(DST_DIR, "entry.png")

os.makedirs(DST_DIR, exist_ok=True)
shutil.copyfile(SRC, DST)
print("wrote " + DST)
