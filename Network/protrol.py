# -*- coding: utf8 -*-

import socket
import threading
import time
import struct
import rlp
from secure.blockchain_crypto import keccak256
from secp256k1 import PrivateKey, PublicKey
from ipaddress import ip_address
import json
from json import JSONDecoder, JSONEncoder


class EndPoint(object):
    def __init__(self, address, udpPort, tcpPort):
        self.address = ip_address(address)
        self.udpPort = udpPort
        self.tcpPort = tcpPort

    def __str__(self):
        return "(EP " + self.address.exploded + " " + str(self.udpPort) + " " + str(self.tcpPort) + ")"

    def pack(self):
        return [self.address.packed, struct.pack(">H", self.udpPort), struct.pack(">H", self.tcpPort)]

    @classmethod
    def unpack(cls, packed):
        udpPort = struct.unpack(">H", packed[1])[0]
        tcpPort = struct.unpack(">H", packed[2])[0]
        return cls(packed[0], udpPort, tcpPort)




# 协议握手
# 1. 节点A --- ping ---> Discover Server
# 2. 节点A <---- pong --- Disconver Server （传输可连接的节点信息，json格式）
# 3. 节点A --- JoinProtrol ---> 节点B
# 4. 节点A <---- WelcomeProtrol --- 节点B

class PingProtrol(object):
    packet_type = '\x01'
    version = '\x03'
    def __init__(self, endpoint_from, endpoint_to, timestamp):
        self.endpoint_from = endpoint_from
        self.endpoint_to = endpoint_to
        self.timestamp = timestamp

    def __str__(self):
        return "(Ping " + str(ord(self.version)) + " " + str(self.endpoint_from) + " " + str(
            self.endpoint_to) + " " + str(self.timestamp) + ")"

    def pack(self):
        return [self.version, self.endpoint_from.pack(), self.endpoint_to.pack(), struct.pack(">I", self.timestamp)]

    @classmethod
    def unpack(cls, packed):
        assert (packed[0] == cls.version)
        endpoint_from = EndPoint.unpack(packed[1])
        endpoint_to = EndPoint.unpack(packed[2])
        timestamp = struct.unpack(">I", packed[3])[0]
        return cls(endpoint_from, endpoint_to, timestamp)



class PongProtrol(object):
    packet_type = '\x02'

    def __init__(self, to, echo, timestamp, ffrom=None):
        self.to = to
        self.echo = echo
        self.timestamp = timestamp
        self.ffrom = ffrom

    def __str__(self):
        return "(Pong " + str(self.to) + " <echo: " + self.echo +  " " + str(self.timestamp) + ")"

    def pack(self):
        return [self.to.pack(), self.echo, struct.pack(">I", self.timestamp)]

    @classmethod
    def unpack(cls, packed):
        to = EndPoint.unpack(packed[0])
        echo = packed[1]
        timestamp = struct.unpack(">I", packed[2])[0]
        return cls(to, echo, timestamp)





class JoinProtrol(PingProtrol):
    packet_type = '\x04'

    def __init__(self, endpoint_from, endpoint_to, timestamp):
        super(JoinProtrol, self).__init__(endpoint_from, endpoint_to, timestamp)


class WelcomeProtrol(PongProtrol):
    packet_type = '\x05'

    def __init__(self, to, echo, timestamp):
        super(WelcomeProtrol, self).__init__(to, echo, timestamp)



class InitNodeProtrol(PongProtrol):
    packet_type = '\x06'

    def __init__(self, to, echo, timestamp):
        super(InitNodeProtrol, self).__init__(to, echo, timestamp)


class ChainMsgProtrol(object):
    packet_type = '\x03'

    def __init__(self, to, msg, timestamp):
        self.to = to
        self.msg = msg
        self.timestamp = timestamp

    def __str__(self):
        return json.dumps(self.msg)

    def pack(self):
        return [self.to.pack(), self.msg, struct.pack(">I", self.timestamp)]

    @classmethod
    def unpack(cls, packed):
        to = EndPoint.unpack(packed[0])
        msg = packed[1]
        timestamp = struct.unpack(">I", packed[2])[0]
        return cls(to, msg, timestamp)












