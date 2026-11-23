"""Load WESAD and prepare labels. Written from the WESAD readme."""
import pickle
from pathlib import Path

# 15 usable people: S2..S17 without S12 (S1 and S12 were discarded by the authors)
SUBJECT_IDS = [i for i in range(2, 18) if i != 12]

# Label meaning from the readme: 0 undefined, 1 baseline, 2 stress, 3 amusement,
# 4 meditation, 5/6/7 ignore. Our two classes: stress = 1, not stress = 0.
LABEL_MAP = {1: 0, 2: 1, 3: 0, 4: 0}

# Wrist (Empatica E4) sampling rates in Hz, from the readme.
WRIST_HZ = {"ACC": 32, "BVP": 64, "EDA": 4, "TEMP": 4}
LABEL_HZ = 700  # labels are sampled at 700 Hz


def load_subject(root, subject_id):
    """Return the dictionary stored in SX.pkl (keys: 'subject', 'signal', 'label')."""
    path = Path(root) / f"S{subject_id}" / f"S{subject_id}.pkl"
    with open(path, "rb") as f:
        return pickle.load(f, encoding="latin1")


def to_binary_label(label_id):
    """Map a WESAD label id to 0 (not stress) / 1 (stress), or None if it must be dropped."""
    return LABEL_MAP.get(int(label_id))


def loso_splits(subject_ids=SUBJECT_IDS):
    """Leave-one-subject-out: yield (train_ids, test_id). The test person is never in train."""
    for test_id in subject_ids:
        train_ids = [s for s in subject_ids if s != test_id]
        yield train_ids, test_id
