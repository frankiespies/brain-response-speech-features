# Correlating Brain Responses with Speech Audio Features

Code for my final-year project in Mechatronic Engineering at Stellenbosch University (2026),
supervised by Prof. Herman Kamper.

The project asks which features of speech the brain follows while a person listens to an audiobook.
EEG from one participant is related to three features of the audio: the speech envelope, acoustic edges
(peakRate, the moments where the envelope rises fastest) and phone onsets from a forced alignment.
Linear models called temporal response functions (TRFs) relate each feature to the EEG, and every
accuracy is compared with an empirical null distribution built by circularly shifting the EEG.

## Main results

Participant P05, scored once on the three held-out test chapters. r is the Pearson correlation between
the predicted and the recorded signal. The corrected threshold is the 95th percentile of the null
distribution of the maximum r across the 63 channels.

| Analysis | Notebook | Result |
|---|---|---|
| Envelope reconstructed from all channels (backward model) | 03 | r = 0.250, p = 0.001 |
| EEG predicted from the envelope (forward model) | 04 | FC5 r = 0.090, corrected threshold 0.057 |
| EEG predicted from peakRate | 05 | FC5 r = 0.083, corrected threshold 0.057 |
| EEG predicted from phone onsets | 06 | FC5 r = 0.105, corrected threshold 0.059 |
| Gain from adding peakRate to the envelope | 05 | FC5 +0.005, p = 0.010 |
| Gain from adding phone onsets to the envelope | 06 | FC5 +0.019, p = 0.005 |

Vowel and consonant onsets can be told apart from the EEG only slightly above chance (balanced accuracy
0.53), and stressed and unstressed vowels not at all (0.50).

## Data

The EEG and audio come from the public dataset *Cortical Tracking of Surprisal during Continuous Speech
Comprehension* on Zenodo: <https://doi.org/10.5281/zenodo.7775260>. Only participant P05 is used.
The data are not included in this repository.

Download the dataset and place it next to the notebooks, so that the folders look like this:

```
repository/
├── config.py
├── 01_preprocess.ipynb ... report_figures.ipynb
├── figures/                      created by the notebooks
└── Data/                         not uploaded to GitHub
    └── Cortical Tracking of Surprisal during Continuous Speech Comprehension/
        ├── P05.h5
        ├── audiobooks/           15 chapter .wav files
        └── stories/story_parts/alignement_data/<chapter>/<chapter>.TextGrid
```

To keep the dataset somewhere else, set the environment variable `EEG_DATA_ROOT` to the dataset folder
before starting Jupyter or VS Code.

`01_preprocess` writes its output inside the dataset folder: `Preprocessed/P05/` (EEG and envelope at
125 Hz, one file per chapter) and `audiobooks/<chapter>_annotations.json` (the forced alignment).

## Setup

Tested with Python 3.12 on Windows.

```
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Running

All paths come from `config.py`. Run `01_preprocess` first; the others only need its output.

| Notebook | What it does | Report |
|---|---|---|
| `01_preprocess` | Filters, re-references and downsamples the EEG, extracts the envelope, converts the TextGrids to JSON and checks the prepared data | Chapters 3 and 4 |
| `02_single_lag_regression` | Reconstructs the envelope from the EEG at one lag at a time; linear and nonlinear regressors | Chapter 4, Appendix A |
| `03_backwardsTRF` | Reconstructs the envelope from all channels over lags of 0 to 392 ms | Chapter 4, Appendix A |
| `04_forwardsTRF` | Predicts each EEG channel from the envelope; TRF shape and scalp maps | Chapter 4 |
| `05_peakRate` | Detects peakRate events, compares them with the syllable structure, models the EEG response and tests the gain over the envelope | Chapter 5, Appendix A |
| `06_phone_onsets` | Builds phone-onset trains, validates the stress labels, models the EEG response and tests timing against phone identity | Chapter 6 |
| `report_figures` | Electrode layout, P1-N1-P2 schematic and feature example | Chapter 2 |

All figures are saved to `figures/` under the names used in the report.

### Cached results

The slowest steps save their results to `Preprocessed/P05/cache/` in the dataset folder: the nonlinear
regressors in `02`, the null distributions of the gain in `05` and `06`, and the detection scan and its
null in `06`. A notebook loads the cache when it exists. To refit instead, set `RECOMPUTE = True` in the
cell that loads the cache (in `06`, in the first cell). On a fresh copy there is no cache, so the first
run computes everything.

### Reproducibility

- The fifteen chapters are split by sorted file name into 9 training, 3 validation and 3 test chapters.
  Model settings are chosen on the validation chapters, and each model is scored once on the test chapters.
- Every random draw uses a fixed seed: `np.random.default_rng(0)`, and seed 1 for the detection null in `06`.
- The first cell of every notebook prints the Python and package versions it ran with.

## Citation

F. A. Spies, *Correlating Brain Responses with Speech Audio Features*, final-year project report,
Stellenbosch University, 2026.