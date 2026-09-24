"""Unpack the reviewed public app bundle; no private desktop files are included."""
from pathlib import Path
import sys
import os
import tempfile
import zipfile
os.environ["OPENBLAS_NUM_THREADS"]="1"
os.environ["OMP_NUM_THREADS"]="1"
_release = tempfile.TemporaryDirectory(prefix="pianivo-code-")
_root = Path(_release.name).resolve()
with zipfile.ZipFile(Path(__file__).with_name("pianivo-web.zip")) as bundle:
    for name in bundle.namelist():
        if not (_root / name).resolve().is_relative_to(_root):
            raise RuntimeError("Invalid bundle path")
    bundle.extractall(_root)
sys.path.insert(0, str(_root))
from render_host import application
