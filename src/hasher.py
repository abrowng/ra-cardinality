import randomhash

def hash_value(count=1, idx=0):
    rfh = randomhash.RandomHashFamily(count=count)
    return lambda x: rfh.hashes(x)[idx]
