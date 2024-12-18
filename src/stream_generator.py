import numpy as np

class DataStreamGenerator:
    def __init__(self, alpha: float, n: int, N: int):
        self.alpha = alpha
        self.n = n
        self.N = N
        self.elements = [f"x{i}" for i in range(1, n + 1)]  # Distinct elements x1, ..., xn
        self.probabilities = self._compute_zipfian_probabilities()

    def _compute_zipfian_probabilities(self):
        normalization_constant = sum(1 / (i ** self.alpha) for i in range(1, self.n + 1))
        probabilities = [(1 / (i ** self.alpha)) / normalization_constant for i in range(1, self.n + 1)]
        return probabilities

    def generate_stream(self):
        stream = np.random.choice(self.elements, size=self.N, p=self.probabilities)
        return list(stream), len(set(stream))