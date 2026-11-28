# Dataset Preparation and Evaluation Methodology

**Project:** Confidence-Aware Stress Support Agent for University Students (Team AI Empire, DCIT 313)
**Issue:** #6 | **Author:** Ibrahim Hidayat (Data and Evaluation Lead) | **Deadline:** 28 November 2026
**Status:** Draft for Milestone 2 report

> This is a wellness prototype, not a medical tool. Nothing in this document describes a diagnosis.

---

## 1. Dataset Acquisition and Preparation Procedure

### 1.1 Source and licence

| Item | Detail |
|---|---|
| Dataset | WESAD (Wearable Stress and Affect Detection) |
| Reference | Schmidt, P., Reiss, A., Duerichen, R., Marberger, C., and Van Laerhoven, K. (2018). *Introducing WESAD, a Multimodal Dataset for Wearable Stress and Affect Detection.* ICMI 2018. |
| Obtained from | The dataset's own public file share (sciebo), linked in the Milestone 1 pitch |
| Date downloaded | 18 July 2026 |
| Licence | The page names no formal licence. It allows use for specific non-commercial purposes if credit is given to the owners. |
| Our use | Non-commercial university coursework. The dataset is cited in every report and README. |

### 1.2 Acquisition steps

1. Download the WESAD archive from the dataset page above.
2. Extract it so that each participant has a folder `S2` to `S17`, each containing a `S<N>.pkl` file.
3. Place the extracted folders in `data/raw/WESAD/` inside the repository.
4. Do **not** commit raw data to GitHub (size and terms of use). The repository's `.gitignore` ignores everything in `data/` except `data/README.md`, and also ignores all `*.pkl` files. The `data/README.md` tells teammates where to download the dataset.
5. Run the preprocessing script (`scripts/`) to produce `data/processed/features.csv`. This file is also ignored by Git, so each teammate regenerates it locally from the raw data.

### 1.3 Participants used

WESAD recorded 17 people. The dataset authors discarded **S1** and **S12** because of sensor malfunction. We therefore use **15 participants (S2 to S17, excluding S12)**, as stated in the Milestone 1 pitch. All 15 are downloaded.

---

## 2. Selected Participants, Sensors and Labels

### 2.1 Sensors

Only the **wrist device (Empatica E4)** is used, because a student could realistically wear it every day. The chest device (RespiBAN) is not used.

| Signal | Meaning | Sampling rate |
|---|---|---|
| BVP | Blood volume pulse (heart-related signal) | 64 Hz |
| EDA | Electrodermal activity (skin conductance) | 4 Hz |
| TEMP | Skin temperature | 4 Hz |
| ACC | 3-axis acceleration (movement) | 32 Hz |

> **Pending verification:** the sampling rates above are the published Empatica E4 specifications and have not yet been checked against the downloaded WESAD files. They will be confirmed once the dataset is available (signal length divided by rate should match the recording duration implied by the 700 Hz labels). Section 3 window sizes depend on these values.

### 2.2 Labels

WESAD labels are stored at 700 Hz alongside the chest data. They are aligned to the wrist signals by time (see 3.2).

| WESAD label | Condition | Our use |
|---|---|---|
| 0 | Not defined / transient | **Dropped** |
| 1 | Baseline | **Not stress** |
| 2 | Stress | **Stress** |
| 3 | Amusement | **Not stress** |
| 4 | Meditation | **Not stress** |
| 5, 6, 7 | Ignored in the WESAD protocol | **Dropped** |

This gives a binary task: **stress (label 2) versus not stress (labels 1, 3, 4)**.

**Class balance note:** stress is the minority class, because baseline, amusement and meditation together last longer than the stress condition. The exact window counts per class and per subject will be computed and reported in a table once preprocessing runs. This imbalance is why accuracy is not used as a headline metric.

---

## 3. Preprocessing and Feature-Extraction Plan

### 3.1 Cleaning

- Load each `S<N>.pkl` and read only the wrist signals and the label array.
- Drop all samples whose label is not in {1, 2, 3, 4}.
- Check for missing values and flat-line signals. Log how many windows are removed per subject and why.
- Windows with too much movement (very high ACC variance) or too few detectable BVP pulse peaks are marked **invalid** and excluded from training and testing. The count is reported. This matches the "invalid input" case in the agent loop (Figure 1 of the pitch).

### 3.2 Windowing

- Each recording is cut into **fixed-length windows** with 50% overlap.
- Candidate window lengths: **30 s, 60 s and 120 s**.
- The final window length is **chosen using training participants only** (see 4.3).
- A window receives a label only if **at least 90% of its samples share one retained label**. Windows that straddle a condition change, or that contain dropped labels, are discarded.
- Label timestamps (700 Hz) are matched to wrist timestamps by elapsed time from recording start.

> Overlap is safe here because every window from one person always goes into the same side of the split (train or test). Windows from the same person are never separated across folds.

### 3.3 Feature extraction

Features are computed **per window, using only that window's samples**. No cross-window or cross-person statistics are used at this stage. The feature set is fixed in advance from the stress-detection literature, not picked by looking at results.

| Sensor | Features |
|---|---|
| BVP | Mean heart rate, SDNN, RMSSD (from detected pulse peaks) |
| EDA | Mean, standard deviation, slope, number of skin-conductance peaks |
| TEMP | Mean, slope |
| ACC | Mean and standard deviation of the magnitude of the 3 axes |

### 3.4 Scaling and feature selection (leakage-sensitive)

- Features are standardised with a **scaler fitted on the training participants only**, then applied unchanged to the held-out participant.
- **No per-person normalisation that uses the test person's own data** (for example, z-scoring each person by their own mean) is used, because it would use information from the held-out participant.
- Because the feature set is fixed in advance, there is no data-driven feature selection. If the team later adds any (for example, removing correlated features), it must be done **inside each fold, on training participants only**.

---

## 4. Leave-One-Subject-Out (LOSO) Evaluation

### 4.1 Procedure

There are **15 outer folds**. In each fold:

1. One participant is held out as the **test person**.
2. The other 14 are the **training people**.
3. Window length, scaler, model and confidence threshold are all decided using the 14 training people only (4.3).
4. The final model is trained on the 14 and evaluated on the held-out person.
5. Results are stored per fold.

After 15 folds, every participant has been the test person exactly once.

### 4.2 Reference implementation of the loop

```python
for test_subject in subjects:                                  # visit each of the 15 people once as the held-out test person
    train_subjects = [s for s in subjects if s != test_subject]  # the other 14 people become the training set
    X_train, y_train = get_data(train_subjects)                # collect features and labels from training people only
    X_test, y_test = get_data([test_subject])                  # collect features and labels from the held-out person

    scaler = StandardScaler().fit(X_train)                     # learn the mean and std from TRAINING data only
    X_train_s = scaler.transform(X_train)                      # scale the training data with those values
    X_test_s = scaler.transform(X_test)                        # scale the test data with the SAME training values (no refit)

    tau = pick_threshold(train_subjects)                       # choose the confidence threshold using an inner loop on training people only
    model = LogisticRegression().fit(X_train_s, y_train)       # train the classifier on the 14 training people
    proba = model.predict_proba(X_test_s)                      # get the probability of each class for each test window
    store_results(test_subject, proba, y_test, tau)            # save outputs so metrics are computed per fold
```

### 4.3 How data leakage is prevented

Anything that is *learned from data* is learned inside the fold, from training people only.

| Decision | Where it is made |
|---|---|
| Scaler (mean and std) | Fitted on the 14 training people |
| Window length | Chosen by an **inner LOSO loop over the 14 training people** (best average F1) |
| Feature set | Fixed in advance (no data-driven selection) |
| Model weights | Trained on the 14 training people |
| **Confidence threshold (tau)** | Chosen by an inner LOSO loop over the 14 training people (see 4.4) |
| Baseline thresholds (one-sensor rule) | Learned on the 14 training people |

Further rules:

- The split is **by person, never by window**. A random window split would put near-identical neighbouring windows from the same person in both train and test and would give falsely high scores.
- The held-out person's labels and signals are **never** used for scaling, threshold choice, window choice or model tuning.
- The test person is touched only once per fold, for final evaluation.
- Random seeds are fixed (see section 8).

### 4.4 Choosing the confidence threshold (training people only)

1. Within the 14 training people, run an inner leave-one-subject-out loop to get honest out-of-fold probabilities for every training window.
2. Try candidate thresholds from 0.50 to 0.95 in steps of 0.05.
3. For each, compute the wrong-confident rate and the hold-back rate on those out-of-fold predictions.
4. Pick the **lowest threshold that keeps the expected cost lowest (using the cost table from the pitch) while holding back no more than a set cap** (proposed cap: 40% of windows).
5. Use that threshold on the held-out person.

> **Team decision needed:** the 40% cap and the cost values are proposals and should be agreed with Jeffery (Agent/System Lead) before runs start.

---

## 5. Baseline Models and Comparison

The pitch states that **the only thing we change is holding back on or off**. So the proposed method uses the same model as baseline 3, with a hold-back rule added.

| # | Model | How it decides | Holds back? | Purpose |
|---|---|---|---|---|
| B1 | Majority class | Always predicts "not stress" | No | Floor. Shows how a model that learns nothing performs on imbalanced data. |
| B2 | One-sensor rule | Predicts stress if mean EDA is above a threshold learned on training people | No | Shows whether a simple single-sensor rule is enough. |
| B3 | Logistic regression (always act) | Predicts the more probable class and always acts | No | Direct comparison point for the proposed method. |
| **P** | **Logistic regression + hold back (proposed)** | Same model as B3, but holds back when the top class probability is below tau | **Yes** | Tests the research question. |

**Comparison table to be filled with LOSO results** (mean and standard deviation over 15 folds). *Pending: results will be added after the dataset is available and the experiments are run. Per-class window counts (section 2.2) are also pending.*

| Model | Stress F1 | Wrong-confident rate | Hold-back rate |
|---|---|---|---|
| B1 Majority class | | | 0 |
| B2 One-sensor rule | | | 0 |
| B3 Logistic regression, always act | | | 0 |
| P Logistic regression + hold back | | | |

**Expected pattern (hypothesis, not a result):** P should show a lower wrong-confident rate than B3, at the price of a higher hold-back rate.

---

## 6. Evaluation Metrics

"Positive" means **stress**. For one held-out person, let *N* = number of valid test windows.

### 6.1 F1-score

F1 of the stress class = 2 x precision x recall / (precision + recall), where precision = TP / (TP + FP) and recall = TP / (TP + FN).

- For always-act models (B1 to B3), computed on all *N* windows.
- For P, computed on the windows where the agent **acted**. Held-back windows are reported separately through the hold-back rate. To make the comparison fair, we also report F1 for P when held-back windows are counted as missed (treated as "not stress"), so readers can see both views.

### 6.2 Confusion matrix

- B1 to B3: 2x2 (true stress / not stress against predicted stress / not stress).
- P: 2x3, with an extra **"held back"** column.
- Matrices are summed over the 15 folds for one pooled matrix, and also reported per person.

### 6.3 Wrong-confident rate

A **wrong-confident decision** is a window where the agent **acted** (confidence at or above tau) and its prediction was **wrong**.

```
wrong-confident rate = (number of acted windows that were wrong) / N
```

We also report this split into confident false alarms (predicted stress, actually not stress) and confident misses (predicted not stress, actually stress). For always-act models, every window counts as acted, so this equals the error rate. This is the **primary metric** for the research question.

### 6.4 Hold-back rate

```
hold-back rate = (number of windows where the agent held back) / N
```

Coverage = 1 minus hold-back rate. This is 0 for B1 to B3.

### 6.5 Cost table

The pitch commits to a cost table for wrong decisions. Each outcome (confident false alarm, confident miss, hold-back, correct action) gets a cost, and expected cost per window is reported. The cost values are agreed by the team and stated explicitly in the report, since they are a design judgement and not a measured quantity.

### 6.6 Aggregation

- Metrics are computed **per held-out person**, then reported as **mean ± standard deviation across the 15 people**.
- Per-person results are shown in a supplementary table, because with only 15 people one unusual person can shift the average.
- No statistical significance claim is made beyond what 15 people can support. Differences are described as observed on WESAD.

---

## 7. Limitations, Ethics and Reproducibility

### 7.1 Dataset limitations

- **Small sample:** only 15 people. Results can change a lot depending on who is in the test set.
- **Lab-induced stress:** stress was created by a lab protocol (a public speaking and arithmetic task), not by real exam or deadline pressure.
- **Not Ghanaian:** the participants were recorded in a European lab. We do **not** claim the data represents University of Ghana students.
- **Narrow demographics:** participants are mostly young adults, with limited variety in age, background and skin tone, which can affect optical sensors such as BVP.
- **Made-up context:** the context inputs (for example, exam week, free minutes) are simulated. Results show whether the method works on WESAD. They do **not** show that suggestions help real students.
- **Movement and sensor noise:** wrist signals are sensitive to motion. Some windows will be invalid and excluded.
- **Short, scripted conditions:** the conditions are a few minutes each in a fixed order, which is unlike everyday life.

### 7.2 Ethical considerations

- **No private student data** is collected, stored or used. WESAD is a published research dataset and all context data is simulated and labelled as such.
- The agent **never diagnoses**. Output is a wellness suggestion, a hold-back message, or a pointer to a real person.
- The agent is not a replacement for professional or human support.
- Acting when unsure is treated as an unacceptable failure. This is why the hold-back mechanism exists.
- Every decision is logged, with no personal identifiers.
- WESAD is credited to its authors (Schmidt et al., 2018), and the non-commercial terms are respected.

### 7.3 Reproducibility

- All code, the feature list, the LOSO loop and the candidate window lengths and thresholds are in this repository.
- Dependencies are pinned in `requirements.txt`.
- Random seeds are fixed in one place and recorded in the results files.
- The raw data is not in the repository. The download source, date and folder layout are documented (section 1).
- Per-fold results (predictions, probabilities, chosen window length and tau) are saved in `results/`, so every number in the report can be traced back.
- The scripts run end to end from raw files to the final comparison table.

---

## 8. Deliverables Checklist (Issue #6)

| # | Deliverable | Section |
|---|---|---|
| 1 | Dataset acquisition and preparation procedure | 1 |
| 2 | Selected participants, sensors and labels | 2 |
| 3 | Preprocessing and feature-extraction plan | 3 |
| 4 | LOSO procedure and leakage prevention | 4 |
| 5 | Baseline vs. confidence-aware comparison table | 5 |
| 6 | Metric definitions and calculations | 6 |
| 7 | Limitations, ethics and reproducibility | 7 |

## References

Schmidt, P., Reiss, A., Duerichen, R., Marberger, C., and Van Laerhoven, K. (2018). Introducing WESAD, a Multimodal Dataset for Wearable Stress and Affect Detection. *Proceedings of the 20th ACM International Conference on Multimodal Interaction (ICMI)*.
