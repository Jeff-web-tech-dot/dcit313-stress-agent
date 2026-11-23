from stress_agent.policy import decide

CTX = {"simulated": True, "exam_week": False, "minutes_free": 15}


def test_abstains_when_unsure():
    assert decide(0.55, CTX, threshold=0.7)["action"] == "abstain"


def test_baseline_never_abstains():
    assert decide(0.55, CTX, threshold=0.5)["action"] == "recommend"


def test_no_action_when_confident_not_stressed():
    assert decide(0.1, CTX)["action"] == "no_action"


def test_refers_after_repeated_flags():
    assert decide(0.95, CTX, recent_flags=2)["action"] == "refer"
