import hashlib
import time

import pytest

from blockchain import Block, Blockchain


def test_block_init():
    '''Test __init__() method of block'''
    # Create test block with known values
    index = 1
    timestamp = int(time.time())
    data = "Test data"
    previous_hash = "abc123"

    # Create block object with attributes
    block = Block(index, timestamp, data, previous_hash)

    # Test read-only attributes of block
    assert block.index == index
    with pytest.raises(AttributeError):
        block.index = 5
    assert block.timestamp == timestamp
    with pytest.raises(AttributeError):
        block.timestamp = "1004503"
    assert block.data == data
    with pytest.raises(AttributeError):
        block.data = "Altered text"
    assert block.previous_hash == previous_hash
    with pytest.raises(AttributeError):
        block.previous_hash = "123456789"
    assert isinstance(block.hash, str)
    assert len(block.hash) == 64
    with pytest.raises(AttributeError):
        block.hash = "987654321"


def test_block_calculate_hash():
    '''Test calculate_hash() method of block'''
    # Create test block with known values
    index = 1
    timestamp = int(time.time())
    data = "Test data"
    previous_hash = "abc123"

    # Create block objetc with atributes
    block = Block(index, timestamp, data, previous_hash)

    # Calculate expected hash
    expected_content = f"{index}{timestamp}{data}{previous_hash}"
    expected_hash = hashlib.sha256(expected_content.encode()).hexdigest()

    # Test hash attribute
    assert block.hash == expected_hash


def test_blockchain_chain():
    '''Test chain attribute of blockchain'''
    # Create blockchain object
    blockchain = Blockchain()

    # Test chain read-only attribute of blockchain
    with pytest.raises(AttributeError):
        blockchain.chain = ["1", "2", "3"]
        

def test_blockchain_add_block():
    '''Test add_block() method of blockchain'''
    # Create blockchain object
    blockchain = Blockchain()

    # Test adding a block without data
    with pytest.raises(ValueError, match="Missing data"):
        blockchain.add_block(None)
        blockchain.add_block("")
        blockchain.add_block([])
        blockchain.add_block({})
        blockchain.add_block(0)
        blockchain.add_block(False)

    # Add block with valid data
    data = "First transaction"
    blockchain.add_block(data)

    # Test block was added
    assert len(blockchain.chain) == 2
    assert blockchain.chain[-1].data == data
