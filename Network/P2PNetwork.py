# -*- coding: utf8 -*-

import socket
import threading
import time
import struct
import rlp
from secure.blockchain_crypto import keccak256
from secp256k1 import PrivateKey, PublicKey
from ipaddress import ip_address
from protrol import *
import os,sys
import traceback


class PingServer(object):
    def __init__(self, my_endpoint):
        self.endpoint = my_endpoint

        ## get private key
        priv_key_file = open('priv_key', 'r')
        priv_key_serialized = priv_key_file.read()
        priv_key_file.close()

        self.priv_key = PrivateKey()
        self.priv_key.deserialize(priv_key_serialized)

        # bind socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', self.endpoint.udpPort))

        # bind tcp socket
        self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpsock.bind(('0.0.0.0', self.endpoint.tcpPort))
        self.tcpsock.listen(10)



    # p2p is the based network
    # so, when the p2p network close
    # the system need to send a quit blockchain msg to Discover server
    def __del__(self):
        pass

    # # hash || signature || packet-type || packet-data
    def wrap_packet(self, packet):
        payload = packet.packet_type + rlp.encode(packet.pack())
        temp = keccak256(payload)
        sig = self.priv_key.ecdsa_sign_recoverable(temp, raw = True)
        sig_serialized = self.priv_key.ecdsa_recoverable_serialize(sig)
        # signature || packet-type || packet-data
        payload = sig_serialized[0] + chr(sig_serialized[1]) + payload
        # hash
        payload_hash = keccak256(payload)
        return payload_hash + payload

    def verifyData(self, data):
        # verify hash
        msg_hash = data[:32]
        if msg_hash != keccak256(data[32:]):
            print " First 32 bytes are not keccak256 hash of the rest."
            return
        else:
            print " Verified message hash."

        # verify signature
        signature = data[32:97]
        signed_data = data[97:]
        deserialized_sig = self.priv_key.ecdsa_recoverable_deserialize(signature[:64], ord(signature[64]))

        remote_pubkey = self.priv_key.ecdsa_recover(keccak256(signed_data), deserialized_sig, raw = True)

        pub = PublicKey()
        pub.public_key = remote_pubkey

        verified = pub.ecdsa_verify(keccak256(signed_data),
                            pub.ecdsa_recoverable_convert(deserialized_sig),
                            raw = True)

        if not verified:
            print " Signature invalid"
            return False
        else:
            print " Verified signature."
            return True

    def recvfrom(self):
        try:
            print "listening..."
            while True :
                data, addr = self.sock.recvfrom(1024)
                print "recvived mssage[", addr, "]"

                res = self.verifyData(data)
                if res:
                    self.dispatch_data(data)
        except:
            traceback.print_exc()
            raise RuntimeError('recvfrom error')

    def recvtcpfrom(self, sock):
        try:
            print "tcp socket listening..."
            while (True):
                data = sock.recv(1024)
                print "【TCP】： get data, data's length is: %d"%len(data)
                res = self.verifyData(data)
                if res:
                    self.dispatch_data(data)
        except:
            traceback.print_exc()
            raise RuntimeError('recvtcpfrom error')

    # 分裂一个进程
    def tcp_listern(self):
        try:
            while True:
                sock, addr = self.tcpsock.accept()
                t = threading.Thread(target=self.recvtcpfrom, args=(sock,))
                t.setDaemon(True)
                t.start()
        except:
            traceback.print_exc()
            raise RuntimeError('tcp_listern error')

    # 分裂一个线程来进行对tcp监听
    def start_tcp_listern(self):
        t = threading.Thread(target=self.tcp_listern)
        t.setDaemon(True)
        t.start()

    def start_udp_listern(self):
        # udp listern
        listern_thread = self.udp_listen()
        listern_thread.start()


    def udp_listen(self):
        thread = threading.Thread(target= self.recvfrom,)
        thread.setDaemon(True)
        return thread

    def rawsendudpmsg(self, endpoint,  message):
        self.sock.sendto(message, (endpoint.address.exploded, endpoint.udpPort))

    # ping send a hello msg
    def ping(self, endpoint):
        ping = PingProtrol(self.endpoint, endpoint, time.time())
        message = self.wrap_packet(ping)
        self.rawsendudpmsg(endpoint, message)

    def pong(self, pongNode):
        message = self.wrap_packet(pongNode)
        self.rawsendudpmsg(pongNode.to, message)


    def dispatch_data(self, data):
        response_types = {
            PingProtrol.packet_type: self.receive_ping,
            PongProtrol.packet_type: self.receive_pong,
            JoinProtrol.packet_type: self.receive_join,
            WelcomeProtrol.packet_type: self.receive_welcome,
            InitNodeProtrol.packet_type: self.receive_initnode,
            ChainMsgProtrol.packet_type: self.receive_msg
        }

        try:
            packet_type = data[97]
            dispatch = response_types[packet_type]
        except:
            print " Unknown message type: " + data[97]
            return

        payload = data[98:]
        dispatch(payload)

    # the function need overrided
    def receive_pong(self, payload):
        print " received Pong"
        print "", PongProtrol.unpack(rlp.decode(payload))

    def receive_ping(self, payload):
        print " received Ping"
        print "", PingProtrol.unpack(rlp.decode(payload))

    def receive_join(self, payload):
        print " received Join"
        print "", JoinProtrol.unpack(rlp.decode(payload))

    def receive_welcome(self, payload):
        print " received welcome"
        print "", JoinProtrol.unpack(rlp.decode(payload))

    def receive_initnode(self, payload):
        print " received initNode"
        print "", JoinProtrol.unpack(rlp.decode(payload))

    def receive_msg(self, payload):
        print " received msg"
        print "", JoinProtrol.unpack(rlp.decode(payload))


    # common function
    @staticmethod
    def SpecialEncode(endpoint):
        temp = {
            'ip': endpoint.address.exploded,
            'port': endpoint.tcpPort
        }
        return json.dumps(temp)

    @staticmethod
    def SpecialDecode(msg):
        return json.loads(msg)


























