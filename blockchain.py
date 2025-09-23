import hashlib
import time


class Block:
    # Initialize block object
    def __init__(self, index, timestamp, data, previous_hash):
        self._index = index
        self._timestamp = timestamp
        self._data = data
        self._previous_hash = previous_hash
        self._hash = self.calculate_hash()

    # Instance method to calculate block hash using sha256
    def calculate_hash(self):
        content = str(self.index) + str(self.timestamp) + self.data + self.previous_hash
        return hashlib.sha256(content.encode()).hexdigest()

    # Expose index as a read-only attribute
    @property
    def index(self):
        return self._index

    # Expose timestamp as a read-only attribute
    @property
    def timestamp(self):
        return self._timestamp

    # Expose data as a read-only attribute
    @property
    def data(self):
        return self._data

    # Expose previous_hash as a read-only attribute
    @property
    def previous_hash(self):
        return self._previous_hash

    # Expose hash as a read-only attribute
    @property
    def hash(self):
        return self._hash


class Blockchain:
    # Initialize blockchain object
    def __init__(self):
        self._chain = [self.create_genesis_block()]

    # Print blockchain
    def __str__(self):
        blockchain_str = "\n"
        for block in self._chain:
            blockchain_str += (
                f"Index: {block.index}\n"
                f"Timestamp: {block.timestamp}\n"
                f"Data: {block.data}\n"
                f"Hash: {block.hash}\n"
                f"Previous hash: {block.previous_hash}\n"
                f"- - - - - - - - - - - - - - -\n"
            )
        return blockchain_str
    
    # Create first block
    def create_genesis_block(self):
        return Block(0, int(time.time()), "Genesis block", "0")

    # Access latest block of the blockchain
    def get_latest_block(self):
        return self._chain[-1]

    # Create and add new block to the blockchain
    def add_block(self, data):
        if not data:
            raise ValueError("Missing data")
        previous_block = self.get_latest_block()
        new_block = Block(len(self._chain), int(time.time()), data, previous_block.hash)
        self._chain.append(new_block)

    # Verify if the chain is correct
    def is_chain_valid(self):
        for i in range(1, len(self._chain)):
            current_block = self._chain[i]
            previous_block = self._chain[i - 1]

            # Check current block hash matches current block hash calculated
            if current_block.hash != current_block.calculate_hash():
                return False
            # Check previous block hash match current block previous block hash
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    # Expose chain as a read-only tuple attribute
    @property
    def chain(self):
        return tuple(self._chain)


def main():
    # Create blockchain object from Blockchain class
    blockchain = Blockchain()

    # Add new block to the blockchain
    blockchain.add_block("First transaction")

    # Print blockchain
    print(blockchain)

    # Verify blockchain
    print(f"Is the blockchain valid? {blockchain.is_chain_valid()}\n")

if __name__ == "__main__":
    main()
