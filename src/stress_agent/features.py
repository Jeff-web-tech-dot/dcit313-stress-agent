"""Turn wrist signals into windows and features. TODO (data and evaluation lead).

Plan:
- Cut each person's recording into fixed-length windows.
- Give each window a label from the 700 Hz label stream (drop windows whose label is 0 or 5-7,
  or that mix labels).
- Compute simple features per window (for example mean and spread of EDA, TEMP, BVP, ACC).
- The window length is chosen using training people only.
"""


def make_windows(*args, **kwargs):
    raise NotImplementedError("TODO: implement windowing")
