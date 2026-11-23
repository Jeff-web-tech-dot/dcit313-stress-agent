from stress_agent.data_loading import SUBJECT_IDS, loso_splits, to_binary_label


def test_fifteen_people():
    assert len(SUBJECT_IDS) == 15
    assert 1 not in SUBJECT_IDS and 12 not in SUBJECT_IDS


def test_test_person_never_in_train():
    rounds = list(loso_splits())
    assert len(rounds) == 15
    for train_ids, test_id in rounds:
        assert test_id not in train_ids


def test_label_mapping():
    assert to_binary_label(2) == 1
    assert to_binary_label(1) == 0 and to_binary_label(3) == 0 and to_binary_label(4) == 0
    assert to_binary_label(0) is None and to_binary_label(6) is None
