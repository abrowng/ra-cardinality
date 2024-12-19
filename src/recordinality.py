import random


class Recordinality:
    def __init__(self, k, hash_function=None):
        self.k = k
        self.hash_function = hash_function
        self.records = []  # Min-heap to store the k largest hashed values
        self.record_count = 0  # Count of k-records (updates to the records table)

    def estimate(self, stream):
        random.shuffle(stream)
        for element in stream:
            hashed_value = self.hash_function(element.replace("\n", ""))
            if hashed_value in self.records:
                continue
            elif len(self.records) < self.k:
                self.records.append(hashed_value)
                self.records.sort()
                self.record_count += 1
            elif hashed_value > self.records[0]:
                # Update the records table if the new hash is larger than the smallest in the table
                self.records = self.records[1:]
                self.records.insert(0, hashed_value)
                self.records.sort()
                self.record_count += 1

        if self.record_count < self.k:
            raise ValueError("Not enough records to estimate cardinality. Process more elements.")

        power_factor = self.record_count - self.k + 1
        estimate = self.k * ((1 + 1 / self.k) ** power_factor) - 1
        return estimate
