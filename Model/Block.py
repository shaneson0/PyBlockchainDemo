

import json

class BlockHeader(object):
    def __init__(self, version, preBlockHash, merkleRoot, timestamp, difficulTarget, nonce):
        self.version = version
        self.preBlockHash = preBlockHash
        self.merkleRoot = merkleRoot
        self.timestamp = timestamp
        self.difficulTarget = difficulTarget
        self.nonce = nonce

    def __str__(self):
        return json.dumps(self.__dict__)

class Block(object):
    def __init__(self, blocksize, blockHeader, transactionCounter, transactions):
        self.blocksize = blocksize
        self.blockHeader = blockHeader
        self.transactionCounter = transactionCounter
        self.transactions = transactions

    def __str__(self):
        return json.dumps(self.__dict__)








