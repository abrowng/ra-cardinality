import argparse
import csv
import os
import random
import sys
from argparse import Namespace

import numpy as np

from src.hasher import hash_value
from src.hyperloglog import HyperLogLog
from src.plotter import Plotter
from src.recardinality import Recordinality
from src.stream_generator import DataStreamGenerator
from src.trial import Trial, Dataset, CardinalityEstimator


FILENAME = "increasing_n"
X_AXIS = "zipf_n"
Y_AXIS = "cardinality"
TITLE = "Cardinality vs Zipf's N"
PLOT = True


TRIALS = [
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=100, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=200, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=300, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=400, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=500, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=600, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=700, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=800, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=900, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=1000, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=2000, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=3000, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=4000, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=5000, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=6000, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=7000, N=100_000, b=3, repetitions=1),
    Trial(estimator=CardinalityEstimator.HLL, dataset=Dataset.RANDOM, alpha=2, n=8000, N=100_000, b=3, repetitions=1),
]


def generate_test_stream(alpha, n, N):
    generator = DataStreamGenerator(alpha, n, N)
    return generator.generate_stream()

def generate_file_stream(filename):
    with open(filename, "r") as f:
        cardinality_counter = set()
        stream = []
        for element in f:
            stream.append(element)
            cardinality_counter.add(element)
        return stream, len(cardinality_counter)


def run_trial(t: Trial, stream: list[str], n: int=10,):
    cardinality_estimates = []
    if t.estimator == CardinalityEstimator.HLL:
        for _ in range(n):
            random_hash_function = hash_value(count=n, idx=random.randint(0, n-1))
            hyper_log_log_estimator = HyperLogLog(t.b, hash_function=random_hash_function)
            for element in stream:
                hyper_log_log_estimator.add(element)
            cardinality_estimates.append(hyper_log_log_estimator.estimate())

    elif t.estimator == CardinalityEstimator.REC:
        for _ in range(n):
            random_hash_function = hash_value(count=n, idx=random.randint(0, n-1))
            rec_estimator = Recordinality(random_hash_function)
            for element in stream:
                rec_estimator.add(element)
            cardinality_estimates.append(rec_estimator.count())

    else:
        raise ValueError(f"Estimator {t.estimator} not supported")

    return cardinality_estimates


def main():

    parser = argparse.ArgumentParser(
        prog="cardinality",
        description="Program used to estimate cardinality of a data "
                    "stream with HyperLogLog and Recordinality algorithms",
    )
    parser.add_argument("operation", choices=["plot", "run"], default="run")
    parser.add_argument("-f", "--filename", default=FILENAME)
    parser.add_argument("-p", "--plot", action="store_true", default=PLOT)

    parser.add_argument(
        "-x",
        help="X-axis data for plotting",
        required=("plot" in sys.argv or PLOT) and X_AXIS is None,
        default=X_AXIS,
    )
    parser.add_argument(
        "-y",
        help="Y-axis data for plotting",
        required=("plot" in sys.argv or PLOT) and Y_AXIS is None,
        default=Y_AXIS,
    )
    parser.add_argument(
        "-t",
        "--title",
        help="Title for the plot",
        required=("plot" in sys.argv or PLOT) and TITLE is None,
        default=TITLE,
    )

    args = parser.parse_args()
    run(args)


def run(args: Namespace):
    if args.operation == "run":
        if not os.path.exists("out"):
            os.makedirs("out")

        with open(f"out/{args.filename}.csv", "w", newline="") as file:
            file.truncate(0)
            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "algorithm", "dataset", "cardinality", "estimate",
                    "filename", "zipf_n", "zipf_N", "zipf_alpha",
                    "hll_b", "bias_correction", "range_correction",
                ],
            )
            writer.writeheader()

        for trial in TRIALS:
            if trial.dataset == Dataset.FILE:
                stream, cardinality = generate_file_stream(trial.filename)
            elif trial.dataset == Dataset.RANDOM:
                stream, cardinality = generate_test_stream(trial.alpha, trial.n, trial.N)
            else:
                raise ValueError(f"Dataset {trial.dataset} not supported")

            estimates = run_trial(trial, stream, trial.repetitions)

            estimated_cardinality = np.mean(estimates)

            with open(f"out/{FILENAME}.csv", "a", newline="") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=[
                        "algorithm", "dataset", "cardinality", "estimate",
                        "filename", "zipf_n", "zipf_N", "zipf_alpha",
                        "hll_b", "bias_correction", "range_correction",
                    ],
                )
                writer.writerow({
                    "algorithm": trial.estimator,
                    "dataset": trial.dataset,
                    "filename": trial.filename,
                    "cardinality": cardinality,
                    "estimate": estimated_cardinality,
                    "zipf_n": trial.n,
                    "zipf_N": trial.N,
                    "zipf_alpha": trial.alpha,
                    "hll_b": trial.b,
                    "bias_correction": trial.bias_correction,
                    "range_correction": trial.range_correction,
                })
            print(f"Estimated cardinality: {estimated_cardinality}")

            print(f"Exact cardinality: {cardinality}")

    if args.operation == "plot" or args.plot:

        plotter = Plotter(f"out/{args.filename}.csv")
        plotter.plot(args.x, args.y, args.title)


if __name__ == "__main__":
    main()
