## 1. Problem Statement

University of Ghana students go through demanding exam and deadline weeks, and a stress-support tool for them needs to be careful about when it speaks up. The team's design rationale is that a system acting on every stress prediction, even when it is unsure, can give a wrong suggestion with false confidence. This project builds a Route B (predictive decision-support) agent that predicts stress or not stress from wrist-sensor data, attaches a confidence score, and acts only when it is fairly sure. When stress looks clear, it offers a short self-care suggestion that fits the context. When it is unsure, it holds back and says so. When stress keeps appearing, it points the student to a real person. The system is a wellness-support prototype, not a medical or diagnostic tool.

Intended beneficiary: University of Ghana students. The agent is designed around a wrist device a student could wear every day. The project does not claim that the WESAD data represents UG students.

Agent task:
- Input: a short window of wrist-sensor readings from WESAD, plus simulated context (for example, exam week and 15 free minutes).
- Decision: logistic regression predicts stress or not stress with a confidence score. If the confidence is high enough, the agent picks a suggestion that fits the context.
- Action: show a short suggestion (for example, a few minutes of slow breathing), hold back and say it is not sure, or suggest talking to someone if stress keeps appearing. Every decision is logged.

## 2. Research Question and Hypothesis

Research question: On WESAD, when each test person is left out of training, does letting the agent hold back when it is unsure reduce wrong confident recommendations compared with always acting on the model's answer?

Hypothesis: Holding back reduces the wrong-confident rate but increases the holdback rate. The only variable changed is whether holding back is on or off.

## 3. Research Objectives

1. Classify stress versus not stress from the WESAD wrist device (BVP, EDA, TEMP, ACC), where stress is label 2 and not stress is labels 1, 3 and 4 (labels 0 and 5 to 7 are dropped). Use short fixed-length windows, with the window length chosen using training participants only.
2. Train a logistic regression model that gives a confidence score for each window, and define a rule for when the agent acts, holds back, or refers the student to a person.
3. Compare the same logistic regression model with holding back on versus off (the only variable changed), and report majority-class and one-sensor-rule baselines for reference.
4. Evaluate with leave-one-subject-out testing (15 rounds), reporting F1, the confusion matrix, the wrong-confident rate, the holdback rate, and a cost table for wrong decisions.
5. Define ethical boundaries and unacceptable failures for the prototype.

## 4. Data and Ethics Pathway

- Dataset: WESAD (Schmidt et al., 2018), 15 usable participants (S2 to S17, excluding S12). The authors discarded S1 and S12 for sensor malfunction. The dataset was downloaded from its own page on 18 July 2026. The page names no formal licence but allows non-commercial use with credit to the owners. This is a non-commercial course project, and the team cites Schmidt et al. (2018).
- Human participants: None. The context inputs (such as exam week and free minutes) are simulated and labelled as such, and are never presented as real user feedback. No private University of Ghana student data is used. Any future user feedback would first be discussed with the lecturer and go through the University's ethics approval process.
- Safeguards: The system is a non-authoritative wellness prototype. It makes no diagnosis, never replaces real help, does not act when unsure, logs every decision, and stores no private data.

## 5. Limitations

- There are only 15 participants.
- The stress was created in a lab, not in real student life.
- The data is not Ghanaian.
- The simulated context cannot show that the advice helps real students, so the results only show whether the method works on WESAD.

## References

Schmidt, P., Reiss, A., Dürichen, R., Marberger, C., & Van Laerhoven, K. (2018). Introducing WESAD, a multimodal dataset for wearable stress and affect detection. In Proceedings of the 20th ACM International Conference on Multimodal Interaction (ICMI '18) (pp. 400-408). ACM. https://doi.org/10.1145/3242969.3242985