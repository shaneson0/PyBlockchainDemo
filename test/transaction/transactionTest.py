

import base58
import struct
import hashlib
import ecdsa
# Alice -> Bob(5BTC) -> Charlie

# https://bitcoin.org/en/developer-reference#raw-transaction-format


#  Bob
# --------- private key --------
# ffd6daeb2f5d259db6e79c8a3139a0f33383468e1916376903e60d2caaaf3f04
# --------- public key ---------
# 04e5632fde54d9edadd04a3b4ffc5713fb2141a05fed5b565c86d0fd3144127867a8501849b7d7b0d653e250a5a5a830129a5ef12d033dd9a80470465c12ad0e16
# --------- Address ---------
# 1sJNDeAEph3Sp4xgZAKRGCyxJizzs2hRi


Bob_address = "1sJNDeAEph3Sp4xgZAKRGCyxJizzs2hRi"
Bob_private_key = "ffd6daeb2f5d259db6e79c8a3139a0f33383468e1916376903e60d2caaaf3f04"
Bob_public_key = "04e5632fde54d9edadd04a3b4ffc5713fb2141a05fed5b565c86d0fd3144127867a8501849b7d7b0d653e250a5a5a830129a5ef12d033dd9a80470465c12ad0e16"
bob_hashed_pubkey = base58.b58decode_check(Bob_address)[1:].encode("hex")

# Alice

# --------- private key --------
# 85c34a0ef7609c8bc903dde81ed017809853ea4ebc2f7ba3479299b01cb060b1
# --------- public key ---------
# 042284580dd9ed26b535bb1f36ecc2f9e86ceb238d863c2a68f7d3be26e33a001d573930085ba100868b6431a3c416c434b0b9ada6ae53429c9b15c0f942cd0168
# --------- Address ---------
# 18YY4qQ1FV5jWS8kFAMq36WCD7bcQ12VmL

Alice_address = "18YY4qQ1FV5jWS8kFAMq36WCD7bcQ12VmL"
Alice_private_key = "85c34a0ef7609c8bc903dde81ed017809853ea4ebc2f7ba3479299b01cb060b1"
Alice_public_key = "042284580dd9ed26b535bb1f36ecc2f9e86ceb238d863c2a68f7d3be26e33a001d573930085ba100868b6431a3c416c434b0b9ada6ae53429c9b15c0f942cd0168"
Alice_hashed_pubkey = base58.b58decode_check(Alice_address)[1:].encode("hex")

# Bob sends 0.001 BTC to Alice and he sends 0.0005 BTC back to himself (change) and the remainder of 0.0005 BTC will be given to miner as a fee


# suppose Bob has his previous transaction that make him has 0.001 BTC


# 1. raw transaction
# 2. raw tx and sign that transaction using my private key (this is the only way o prove that I'm Bob)
# 3. raw tx and sign in order to create the real transaction


prv_txid = "84d813beb51c3a12cb5d0bb18c6c15062453d476de24cb2f943ca6e20115d85c"


class raw_tx:
    version = struct.pack("<L", 1)
    tx_in_count = struct.pack("<B",1)
    tx_in = {}
    tx_out_count = struct.pack("<B", 2)
    tx_out1 = {}
    tx_out2 = {}
    lock_time = struct.pack("<L", 0)

def flip_byte_order(string):
    flipped = "".join(reversed([string[i:i+2] for i in range(0, len(string), 2)]))
    return flipped

# input transaction
rtx = raw_tx()
rtx.tx_in["txouthash"] = flip_byte_order(prv_txid).decode("hex")
rtx.tx_in["tx_out_index"] = struct.pack("<L", 0)
rtx.tx_in["script"] = ("76a914%s88ac"%bob_hashed_pubkey).decode("hex")
rtx.tx_in["script_bytes"] = struct.pack("<B", len(rtx.tx_in["script"]))
rtx.tx_in["sequence"] = "ffffffff".decode("hex")


# output transaction

rtx.tx_out1["value"] = struct.pack("<Q", 100000)
rtx.tx_out1["pk_script"] = ("76a914%s88ac"%Alice_hashed_pubkey).decode("hex")
rtx.tx_out1["pk_script_bytes"] = struct.pack("<B", len(rtx.tx_out1["pk_script"]))


# Bob 's transaction fee
rtx.tx_out2["value"] = struct.pack("<Q", 50000)
rtx.tx_out2["pk_script"] = ("76a914%s88ac"%bob_hashed_pubkey).decode("hex")
rtx.tx_out2["pk_script_bytes"] = struct.pack("<B", len(rtx.tx_out2["pk_script"]))


raw_tx_string = (
    rtx.version
    + rtx.tx_in_count
    + rtx.tx_in["txouthash"]
    + rtx.tx_in["tx_out_index"]
    + rtx.tx_in["script"]
    + rtx.tx_in["script_bytes"]
    + rtx.tx_in["sequence"]
    + rtx.tx_out_count
    + rtx.tx_out1["value"]
    + rtx.tx_out1["pk_script_bytes"]
    + rtx.tx_out1["pk_script"]
    + rtx.tx_out2["value"]
    + rtx.tx_out2["pk_script_bytes"]
    + rtx.tx_out2["pk_script"]
    + rtx.lock_time
    + struct.pack("<L", 1)
)

hashed_tx_to_sign = hashlib.sha256( hashlib.sha256(raw_tx_string).digest() ).digest()
sk = ecdsa.SigningKey.from_string(Bob_private_key.decode("hex"), curve = ecdsa.SECP256k1)
vk = sk.verifying_key
public_key = ('\04' + vk.to_string()).encode("hex")
signature = sk.sign_digest(hashed_tx_to_sign, sigencode = ecdsa.util.sigencode_der)


sigscript = (
    signature
    + "\01"
    + struct.pack("<B", len(public_key.decode("hex")))
    + public_key.decode("hex")
)

real_tx = (
    rtx.version
    + rtx.tx_in_count
    + rtx.tx_in["txouthash"]
    + rtx.tx_in["tx_out_index"]
    + struct.pack("<B", len(sigscript) + 1)
    + struct.pack("<B", len(signature) + 1)
    + sigscript
    + rtx.tx_in["sequence"]
    + rtx.tx_out_count
    + rtx.tx_out1["value"]
    + rtx.tx_out1["pk_script_bytes"]
    + rtx.tx_out1["pk_script"]
    + rtx.tx_out2["value"]
    + rtx.tx_out2["pk_script_bytes"]
    + rtx.tx_out2["pk_script"]
    + rtx.lock_time
)

print len(sigscript) + 1
print len(signature) + 1
print rtx.tx_out1["value"]
print real_tx.encode("hex")


# 01000000      --- Version
# 01            --- Number of inputs
# 5cd81501e2a63c942fcb24de76d4532406156c8cb10b5dcb123a1cb5be13d884  ---- Outpoint TXID
# 00000000                                                          ---- tx_out_index
# 8b                                                                ---- sigscript's len
# 48                                                                ---- signature's len
# 3045022029cf4e5b864ccd3259bae9338ea7a099d3d669d09fddd3
# 0e05489607fbc3dc9d0221009e7f2a2a1d69dfc8165defa8c3298e
# 291e287b6dcd361f40bf76f11880219acd014104e5632fde54d9ed
# add04a3b4ffc5713fb2141a05fed5b565c86d0fd3144127867a850
# 1849b7d7b0d653e250a5a5a830129a5ef12d033dd9a80470465c12
# ad0e16                                                            ---- Secp256k1 signature
# ffffffff                                                          ---- Sequence number:
# 02                                                                ---- output count
# 313030303030                                                      ---- Satoshis
# 19
# 76a91452bfb53e84f461fe6c2145fd7eaf25800103b05188ac
# --- out2's script ---
# 3530303030
# 19
# 76a91409834b5a9e617040ce6e405a49dda4069306ba2088ac

# 00000000        ------------ locktime

#  ------------------- send out transaction ------------------

real_tx = real_tx.decode("hex")
tx_command = "tx" + 10 * "\00"

tx_len = struct.pack("L", len(real_tx))
tx_checksum = hashlib.sha256(hashlib.sha256(real_tx).digest()).digest()[:4]

# tx_msg = magic + tx_command + tx_len + tx_checksum + real_tx







