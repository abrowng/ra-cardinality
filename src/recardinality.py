import math

class Recordinality:
    def __init__(self, hash_function, p=14):
        self.hash_function = hash_function
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m

    def add(self, element):
        hash_value = self.hash_function(element)
        index = hash_value & (self.m - 1)
        register_value = self.registers[index]
        if register_value == 0:
            self.registers[index] = 1
        elif register_value < math.log2(1.0 / (hash_value >> (self.p - index))):
            self.registers[index] = math.log2(1.0 / (hash_value >> (self.p - index)))

    def count(self):
        estimate = sum(2.0 ** (-register_value) for register_value in self.registers)
        estimate = (1 << self.p) * math.log2(1.0 / estimate)
        return estimate