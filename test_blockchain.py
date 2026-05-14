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
    for missing_data in (None, "", [], {}, 0, False):
        with pytest.raises(ValueError, match="Missing data"):
            blockchain.add_block(missing_data)

    # Test adding non-string data
    for invalid_data in (["transaction"], {"transaction": 1}, 100, True):
        with pytest.raises(TypeError, match="Block data must be a string"):
            blockchain.add_block(invalid_data)

    # Add block with valid data
    data = "First transaction"
    blockchain.add_block(data)

    # Test block was added
    assert len(blockchain.chain) == 2
    assert blockchain.chain[-1].data == data


def test_blockchain_add_block_links_to_previous_block():
    '''Test add_block() links new blocks to the current latest block'''
    blockchain = Blockchain()
    previous_block = blockchain.get_latest_block()

    blockchain.add_block("First transaction")
    new_block = blockchain.get_latest_block()

    assert new_block.index == 1
    assert new_block.previous_hash == previous_block.hash


def test_blockchain_is_chain_valid():
    '''Test is_chain_valid() detects valid and tampered chains'''
    blockchain = Blockchain()
    blockchain.add_block("First transaction")
    blockchain.add_block("Second transaction")

    assert blockchain.is_chain_valid() is True

    blockchain._chain[1]._data = "Altered transaction"

    assert blockchain.is_chain_valid() is False
