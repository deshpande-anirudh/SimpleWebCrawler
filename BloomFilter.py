from bitarray import bitarray
import murmurhash

class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = bitarray(size)
        self.bit_array.setall(0)

    def _hash_positions(self, item: str):
        hash_positions = []
        for i in range(self.num_hashes):
            pos = abs(murmurhash.hash(item, seed=i)) % self.size
            hash_positions.append(pos)
        return hash_positions

    def add(self, item: str):
        for pos in self._hash_positions(item):
            self.bit_array[pos] = 1

    def contains(self, item: str) -> bool:
        return all(self.bit_array[pos] for pos in self._hash_positions(item))

# Example Usage
bf = BloomFilter(size=1000, num_hashes=3)

bf.add("apple")
bf.add("banana")

print("apple:", bf.contains("apple"))  # True
print("banana:", bf.contains("banana"))  # True
print("cherry:", bf.contains("cherry"))  # False
