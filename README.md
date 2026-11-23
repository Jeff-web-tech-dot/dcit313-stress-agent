# Confidence-Aware Stress Support Agent for University Students

DCIT 313 (Introduction to AI) semester project, University of Ghana, 2026/2027.
Team: AI Empire

This is a **wellness prototype, not a medical tool**. It does not diagnose anything.

## What it does
A small agent that reads wrist-sensor features, predicts stress or not stress with a
confidence score, and then chooses one action: suggest a short self-care step, hold
back (abstain), or point to a real person. Every decision is logged.

**Research question:** On WESAD, with each test person left out of training, does letting
the agent hold back when it is unsure reduce wrong confident recommendations compared
with always acting on the model's answer?

## Team and roles
| Role | Name | Main folders |
|---|---|---|
| Problem and ethics lead |Princess Sarah Atafiri | docs/ |
| Data and evaluation lead | | src/stress_agent/data_loading.py, features.py, evaluate.py, scripts/ |
| Agent and system lead |Jeffery Anyimah Kwasi | src/stress_agent/models.py, policy.py, context_sim.py, agent.py |
| Software and testing lead | | tests/, README, requirements, repo health |
| Research and reporting lead | | docs/ (logs, related work, report) |

## Folder map
```
data/          WESAD goes here on your own computer (NOT uploaded, see data/README.md)
docs/          pitch, proposal, datasheet, system card, weekly log, decision log, AI-use log
src/stress_agent/   the code: data loading, features, models, policy, simulated context, agent
scripts/       scripts that produce every results table
tests/         automated tests
results/       tables/ and figures/ made by the scripts
notebooks/     exploration only (final results must come from scripts/)
```

## Set up (step by step)
1. Install Python 3.10 or newer.
2. `git clone <repo link>` then `cd` into the folder.
3. Create an environment: `python -m venv .venv`
4. Activate it. Windows: `.venv\Scripts\activate`  Mac/Linux: `source .venv/bin/activate`
5. `pip install -r requirements.txt`
6. Download WESAD yourself and put it in `data/WESAD/` (see `data/README.md`).
7. Run the tests: `pytest`

## Data and terms of use
Dataset: WESAD (Schmidt, Reiss, Duerichen, Marberger, Van Laerhoven, "Introducing WESAD, a
multimodal dataset for Wearable Stress and Affect Detection", ICMI 2018,
https://doi.org/10.1145/3242969.3242985).
The download page allows use for scientific, non-commercial purposes with credit to the
owners. No named licence is given. The dataset is not stored in this repo.
Context data (exam week, free minutes) is **simulated** and always labelled as simulated.
No human participants and no private student data are used.

## Status
See `docs/weekly_log.md`.
