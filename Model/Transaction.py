
import json

class TransactionModel(object):
    def __init__(self, txhash, iscoinbase, blockhash, publickey, amount, output):
        self.txHash = txhash
        self.isCoinBase = iscoinbase
        self.blockHash = blockhash
        self.publicKey = publickey
        self.amount = amount
        self.output = output

    def __str__(self):
        return json.dumps(self.__dict__)


class TransactionIndex(object):
    def __init__(self, blockHash, blockOffsets, transactionOffset):
        self.blockHash = blockHash
        self.blockOffsets = blockOffsets
        self.transactionOffset = transactionOffset

    def __str__(self):
        return json.dumps(self.__dict__)
















