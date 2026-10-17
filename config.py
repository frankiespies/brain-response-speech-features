"""Paths shared by all notebooks.

By default the dataset is expected in Data/ next to this file (see README.md).
To keep it elsewhere, set the environment variable EEG_DATA_ROOT to the
dataset folder before starting Jupyter or VS Code.
"""
import os
import platform
from pathlib import Path

REPO = Path(__file__).resolve().parent

DATA_ROOT = Path(os.environ.get(
    "EEG_DATA_ROOT",
    REPO / "Data" / "Cortical Tracking of Surprisal during Continuous Speech Comprehension",
))

PARTICIPANT = "P05"

PREPROCESSED = DATA_ROOT / "Preprocessed" / PARTICIPANT   # written by 01_preprocess
AUDIOBOOKS = DATA_ROOT / "audiobooks"                       # chapter audio and *_annotations.json
ALIGNMENT = DATA_ROOT / "stories" / "story_parts" / "alignement_data"   # spelling as in the dataset
FIGURES = REPO / "figures"                                  # every figure in the report
CACHE = PREPROCESSED / "cache"                              # results of the slow refits

if not DATA_ROOT.is_dir():
    raise FileNotFoundError(
        f"Dataset not found at {DATA_ROOT}.\n"
        "Download it as described in README.md, or set EEG_DATA_ROOT to its folder."
    )

for _d in (PREPROCESSED, FIGURES, CACHE):
    _d.mkdir(parents=True, exist_ok=True)


def print_versions():
    """Print the Python and package versions, so a run can be matched to requirements.txt."""
    import importlib
    names = ["numpy", "scipy", "sklearn", "mne", "h5py", "matplotlib"]
    parts = [f"Python {platform.python_version()}"]
    for n in names:
        try:
            parts.append(f"{n} {importlib.import_module(n).__version__}")
        except ImportError:
            parts.append(f"{n} missing")
    print(" | ".join(parts))