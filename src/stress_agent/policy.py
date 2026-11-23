"""The decision rule: what the agent does with the model's answer.

Actions: "recommend", "no_action", "abstain", "refer".
Set threshold = 0.5 to get the baseline that always acts (it never abstains).
"""

REFER_AFTER = 3  # refer to a person after this many stress flags in a row


def decide(p_stress, context, recent_flags=0, threshold=0.7):
    """p_stress: model probability of stress (0 to 1).
    context: dict from context_sim.
    recent_flags: how many stress flags in a row came before this one.
    threshold: minimum confidence needed to act.
    """
    confidence = max(p_stress, 1 - p_stress)
    if confidence < threshold:
        return {"action": "abstain", "reason": "not sure enough", "confidence": confidence}
    if p_stress >= 0.5:
        if recent_flags + 1 >= REFER_AFTER:
            return {"action": "refer", "reason": "stress keeps appearing; suggest talking to a person",
                    "confidence": confidence}
        if context.get("minutes_free", 0) >= 10:
            step = "5 minutes of slow breathing"
        else:
            step = "a 1-minute pause"
        return {"action": "recommend", "reason": step, "confidence": confidence}
    return {"action": "no_action", "reason": "no stress signs", "confidence": confidence}
