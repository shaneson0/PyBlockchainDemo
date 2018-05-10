# -*- coding: utf8 -*-

import hashlib
import sha3
import os
import ecdsa
import base58

# 以太坊使用keccak-256哈希算法

def keccak256(s):
    k = sha3.keccak_256()
    k.update(s)
    return k.digest()

def create_private_key():
    private_key = os.urandom(32).encode("hex")
    return private_key

def create_public_key(privateKey):
    sk = ecdsa.SigningKey.from_string(privateKey.decode("hex"), curve = ecdsa.SECP256k1)
    vk = sk.verifying_key
    return ('\x04' + vk.to_string()).encode("hex")

def publicKey_to_address(publicKey):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update( hashlib.sha256(publicKey.decode('hex')).digest())
    middle_man = '\x00' + ripemd160.digest()
    checksum = hashlib.sha256( hashlib.sha256(middle_man).digest() ).digest()[:4]
    binary_add = middle_man + checksum
    addr = base58.b58encode(binary_add)
    return addr

# return bool
def signMsg(private_key, msg):
    sk = ecdsa.SigningKey.from_string(private_key.decode("hex"), curve = ecdsa.SECP256k1)
    vk = sk.verifying_key
    signed_msg = sk.sign(msg)
    return signed_msg

def vertify_msg(private_key, signed_msg, msg):
    sk = ecdsa.SigningKey.from_string(private_key.decode("hex"), curve = ecdsa.SECP256k1)
    vk = sk.verifying_key
    res = vk.verify(signed_msg, msg)
    return res


# PublicKey in the bitaddress.org is
# 045039541bc99c3d30c0f4e4684e4ce0686b00613c7d5c2bdf6d677e1b3d7bd4e045ae1739503df5742a82019b73f946fef0df982caa3808b36a734a869d698a16

# PrivateKey is
# 5888612fb46df38e81d3c724b6276933c451e98895a5973368f37659ce72d7e9

# Address is
# 14tcrCrYJXRqVA6wnS6Ns7jhgZcfDpyJu2

if __name__ == "__main__":
    priKey = create_private_key()
    print '--------- private key --------'
    print priKey
    print '--------- public key ---------'
    publicKey = create_public_key(priKey)
    print publicKey
    print '--------- Address ---------'
    addr = publicKey_to_address(publicKey)
    print addr
    
    # publicKey = "045039541bc99c3d30c0f4e4684e4ce0686b00613c7d5c2bdf6d677e1b3d7bd4e045ae1739503df5742a82019b73f946fef0df982caa3808b36a734a869d698a16"
    # addr = publicKey_to_address(publicKey)
    # print '--------- address ---------'
    # print addr

    # private_key = "5888612fb46df38e81d3c724b6276933c451e98895a5973368f37659ce72d7e9"
    # print '------ verify msg ------'
    # msg = "hello world"
    # sinagure = signMsg(private_key, msg)
    # print "res: ", vertify_msg(private_key, sinagure, msg)






