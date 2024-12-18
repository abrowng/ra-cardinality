import math


class HyperLogLog:
    def __init__(self, b: int, hash_function=None, hash_bits=32, range_correction=True, bias_correction=True):
        self._hash = hash_function
        self.b = b
        self.m = 1 << b  # Number of buckets (2^b)
        self.buckets = [0] * self.m
        self.hash_bits = hash_bits
        self.range_correction = range_correction
        self.bias_correction = bias_correction

    def count_zeros(self, hash_value):
        zeros = 0
        while hash_value:
            if hash_value & 1 << 0 == 0:
                zeros += 1
                hash_value >>= 1
                continue
            break
        return zeros

    def add(self, value):
        x = self._hash(value)
        # Extract the first b bits as bucket index
        j = x >> (self.hash_bits - self.b)
        self.buckets[j] = max(self.buckets[j], self.count_zeros(x))

    def estimate(self):
        # HyperLogLog bias-corrected constant
        alpha_m = 0.7213 / (1 + 1.079 / self.m)
        if self.bias_correction:
            # Values from the HyperLogLog paper by Flajolet et al.
            if self.m == 4:
                alpha_m = 0.532
            elif self.m == 8:
                alpha_m = 0.626
            elif self.m == 16:
                alpha_m = 0.673
            elif self.m == 32:
                alpha_m = 0.697
            elif self.m == 64:
                alpha_m = 0.709

        Z = sum(2 ** -bucket for bucket in self.buckets)
        E = alpha_m * (self.m ** 2) / Z

        if self.range_correction:
            if E <= 2.5 * self.m:  # Small range correction
                V = self.buckets.count(0)
                if V > 0:
                    E = self.m * math.log(self.m / V)
            elif E > (1 << 32) / 30:  # Intermediate range correction
                E = E
            else:  # Large range correction
                E = -(1 << 32) * math.log(1 - E / (1 << 32))

        return int(E)