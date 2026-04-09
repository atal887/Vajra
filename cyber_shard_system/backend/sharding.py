def split_into_shards(data, num_shards):
    shard_size = len(data) // num_shards
    shards = []

    for i in range(num_shards):
        start = i * shard_size
        end = None if i == num_shards - 1 else (i + 1) * shard_size
        shards.append(data[start:end])

    return shards


def generate_parity(shard1, shard2):
    parity = bytearray(len(shard1))

    for i in range(len(shard1)):
        parity[i] = shard1[i] ^ shard2[i]

    return bytes(parity)