import sys
sys.path.append("..")

import json
from secure import blockchain_crypto
from Util import fileUtil



class wallet(object):
    def createWallet(self):
        try:
            priKey = blockchain_crypto.create_private_key()
            publicKey = blockchain_crypto.create_public_key(priKey)
            addr = blockchain_crypto.publicKey_to_address(publicKey)

            # write file
            fileUtil.writeFile("private_key")
            fileUtil.writeFile("public_key")
            fileUtil.writeFile("address")
            return True, priKey, publicKey, addr
        except:
            return False, "", "", ""

    def doTransaction(self):
        pass

    def saveWallet(self):
        pass














































