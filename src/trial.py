from __future__ import annotations

from collections import namedtuple
from enum import Enum

FIELDS = [
    "estimator", "dataset", "filename",         # General settings
    "alpha", "n", "N",                          # Zipf stream settings
    "b", "bias_correction", "range_correction", # HyperLogLog settings
    "k",                                        # Recordinality settings
    "repetitions",                              # Output settings
    "hash_family",
]

DEFAULT_VALUES = (
    None, None, None, 1, 1, 1, 2, True, True, 1, 10, None
)


class Dataset(Enum):
    FILE = "file"
    RANDOM = "random"


class CardinalityEstimator(Enum):
    HLL = "hll"
    REC = "rec"


class Trial(namedtuple("Trial", field_names=FIELDS, defaults=DEFAULT_VALUES)):

    estimator: CardinalityEstimator
    dataset: Dataset
    filename: str
    alpha: float
    n: int
    N: int
    b: int
    k: int
    repetitions: int
    bias_correction: bool
    range_correction: bool
    hash_family: str
