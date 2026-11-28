## 2. Related Work and Novelty

We reviewed five works. The full review is in `docs/literature/`.

| Study | What it did | Data | Main result | Limit for our purpose |
|---|---|---|---|---|
| Schmidt et al. (2018), WESAD | Lab protocol with chest and wrist sensors; benchmark with standard machine learning | 15 usable people (17 took part) | Up to 80% (three classes) and up to 93% (stress vs non-stress) accuracy | Small lab sample; no support agent and no confidence-based response |
| Shvetcov et al. (2024) | Supervised machine learning on passive smartphone data to predict stress | 409 university students, 30 days | Passive sensing can digitally phenotype stress in university students | Smartphone data, not wearable signals; unable to phenotype mild-to-moderate stress; no support action |
| Neigel et al. (2025) | Smart-ring data compared with the academic calendar | 103 Japanese university students, up to 28 months | Stress-related patterns appear around exam periods | Group-level patterns, not individual decisions |
| Garcia-Ceja et al. (2026) | Dataset paper: daily self-reports with Fitbit data | Undergraduates at two Mexican universities, one semester | Public student dataset with over 80% questionnaire compliance | Dataset only; no prediction model reported |
| Fisch et al. (2022) | Selective calibration: a selector rejects predictions with unreliable confidence | Image and lung-cancer risk tasks | Better calibration among accepted predictions | Not tested on stress or wearable data |

### Novelty matrix

| Capability | WESAD | Shvetcov | Neigel | Garcia-Ceja | Fisch | Our agent |
|---|---|---|---|---|---|---|
| Stress from wearable signals | Yes (benchmark) | No (phone data) | Group patterns | Data only | No | Planned (WESAD wrist) |
| Student focus | No | Yes | Yes | Yes | No | Use-case only; WESAD is not student data |
| Real-world data | No (lab) | 30 days | Up to 28 months | One semester | n/a | No (lab data) |
| Support action from the prediction | No | No | No | No | No | Planned (simulated context, rules) |
| Confidence score used | Not central | Not central | Not central | No | Yes (method) | Planned (model probability) |
| Holds back when unsure | Not reported | Not reported | Not reported | Not reported | Yes (method) | Planned (simple threshold) |

"Planned" means a design goal, not a result.

### Gap
In these five works we found no example that classifies stress from wearable signals, estimates how reliable that estimate is, and changes what it does according to that reliability. This is a gap in this set of papers. It does not show that no such system exists anywhere. Our abstention rule is a simple confidence threshold, not Fisch et al.'s selective calibration. Because WESAD is not student data and the context is simulated, we can only show whether the method works on WESAD, not whether it helps UG students.

### References
Fisch, A., Jaakkola, T., & Barzilay, R. (2022). Calibrated selective classification. *Transactions on Machine Learning Research*. https://openreview.net/forum?id=zFhNBs8GaV

Garcia-Ceja, E., Alvarado-Uribe, J., Escamilla-Ambrosio, P. J., Lara, A., Mena-Martinez, A., Gallegos-Garcia, G., Gonzalez-Mendoza, M., Monroy, R., Martinez Luna, G., & Fernández-Cárdenas, J. M. (2026). A dataset of university students' stress and anxiety levels based on questionnaires and wearable sensors. *Scientific Data, 13*, Article 732. https://doi.org/10.1038/s41597-026-07085-7

Neigel, P. N., Vargo, A., Tag, B., & Kise, K. (2025). Unobtrusive stress detection using wearables: Application and challenges in a university setting. *Frontiers in Computer Science, 7*, 1575404. https://doi.org/10.3389/fcomp.2025.1575404

Schmidt, P., Reiss, A., Dürichen, R., Marberger, C., & Van Laerhoven, K. (2018). Introducing WESAD, a multimodal dataset for wearable stress and affect detection. In *Proceedings of the 2018 International Conference on Multimodal Interaction* (pp. 400–408). ACM. https://doi.org/10.1145/3242969.3242985

Shvetcov, A., Funke Kupper, J., Zheng, W.-Y., Slade, A., Han, J., Whitton, A., Spoelma, M., Hoon, L., Mouzakis, K., Vasa, R., Gupta, S., Venkatesh, S., Newby, J., & Christensen, H. (2024). Passive sensing data predicts stress in university students: A supervised machine learning method for digital phenotyping. *Frontiers in Psychiatry, 15*, 1422027. https://doi.org/10.3389/fpsyt.2024.1422027
