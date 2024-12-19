import hashlib
import random

import randomhash
import xxhash


def hash_func(count=1, idx=0, hash_family="CRC32"):
    seed = random.randint(100000, 20241218 * (idx + 1))

    if hash_family == "CRC32":
        h = randomhash.RandomHashFamily(count=count)
        return lambda x: h.hashes(x)[idx]
    elif hash_family == "xxHash32":
        def hash_value(x):
            h = xxhash.xxh32("", seed=seed)
            h.update(x)
            return h.intdigest()
        return hash_value
    elif hash_family == "SHA256":
        def hash_value(x):
            h = hashlib.sha256(str(seed).encode())
            h.update(x.encode())
            hex_digest = h.hexdigest()
            return int(hex_digest, 16) & ((1 << 32) - 1)
        return hash_value
    elif hash_family == "MD5":
        def hash_value(x):
            h = hashlib.md5(str(seed).encode())
            h.update(x.encode())
            hex_digest = h.hexdigest()
            return int(hex_digest, 16) & ((1 << 32) - 1)
        return hash_value
    elif hash_family == "none":
        return lambda x: int.from_bytes(x.encode(), byteorder="big")
