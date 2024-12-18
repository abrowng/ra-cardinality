from __future__ import annotations

from collections import namedtuple
from enum import Enum

FIELDS = [
    "estimator", "dataset", "filename",         # General settings
    "alpha", "n", "N",                          # Zipf stream settings
    "b", "bias_correction", "range_correction", # HyperLogLog settings
    "repetitions",                              # Output settings
]


class Dataset(Enum):
    FILE = "file"
    RANDOM = "random"


class CardinalityEstimator(Enum):
    HLL = "hll"
    REC = "rec"


class Trial(namedtuple("Trial", field_names=FIELDS, defaults=(None,) * len(FIELDS))):

    estimator: CardinalityEstimator
    dataset: Dataset
    filename: str
    alpha: float
    n: int
    N: int
    b: int
    repetitions: int
    bias_correction: bool = True
    range_correction: bool = True
