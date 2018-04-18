# -*- coding: utf8 -*-



import random
import socket
from P2PNetwork import PingServer
from protrol import *

# 挖矿节点
# 挖矿节点的功能主要是
# 1. 由pong收到连接的地址之后，开始使用tcp连接到该地址的tcp服务
# 2. 使用neighbour数组来记录邻居情况
# 3. 使用tcp进行挖矿处理

class MinerNode(PingServer):
    def __init__(self, endpoint):
        super(MinerNode, self).__init__(endpoint)
        # 存储endpoint
        # neighbours是一个{neighter: socket}这个结构的
        self.neighbours = {}

    def addNeighbour(self, neighbour):
        s = self.connectNeighbour(neighbour)
        print 'add Neighbour: %s'%neighbour
        self.neighbours[neighbour] = s

    def getNeighbours(self):
        templist = self.neighbours.items()
        (address, _socket) = templist[0]
        return address


    def connectNeighbour(self, tempneighbour):
        neighbour = MinerNode.SpecialDecode(tempneighbour)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((neighbour['ip'], neighbour['port']))
        return s

    def rawsendtcpmsg(self, endpoint,  message):
        neighbour = PingServer.SpecialEncode(endpoint)
        s = self.neighbours[neighbour]
        s.send(message)
        # self.sock.sendto(message, (endpoint.address.exploded, endpoint.tcpPort))

    def join(self, Address):
        to = EndPoint(Address['ip'], 0,  Address['port'])
        # endpoint_from, endpoint_to, timestamp
        joinprotrol = JoinProtrol(self.endpoint, to, time.time())
        message = self.wrap_packet(joinprotrol)
        print '【Join】： rawsendtcpmsg， to: ',(to.address.exploded, to.tcpPort)
        self.rawsendtcpmsg(to, message)

    # 对来join入网络的节点表示欢迎
    def welcome(self, to):
        fromMsg = MinerNode.SpecialEncode(self.endpoint)
        welcomeprotrol = WelcomeProtrol(to, fromMsg, time.time())
        message = self.wrap_packet(welcomeprotrol)
        self.rawsendtcpmsg(to, message)

    def chat(self, to):
        msg = "hello I'm shanxuan"
        Chainmsg = ChainMsgProtrol(to, msg, time.time())
        message = self.wrap_packet(Chainmsg)
        self.rawsendtcpmsg(to, message)



    # 由pong收到连接的地址之后，开始使用tcp连接到该地址的tcp服务
    def receive_pong(self, payload):
        print "Miner received pong"
        Pongmsg = PongProtrol.unpack(rlp.decode(payload))
        # before join the p2pnetwork, need to connect the socket
        self.addNeighbour(Pongmsg.echo)
        # join
        PongObject = MinerNode.SpecialDecode(Pongmsg.echo)
        self.join(PongObject)

    # 加入邻居节点
    def receive_join(self, payload):
        print "Miner received join"
        JoinMsg = JoinProtrol.unpack(rlp.decode(payload))
        endpoint_from = JoinMsg.endpoint_from
        self.addNeighbour(MinerNode.SpecialEncode(endpoint_from))


    def receive_welcome(self, payload):
        print "Miner received welcome"
        welcomeMsg = WelcomeProtrol.unpack(rlp.decode(payload))
        self.addNeighbour(welcomeMsg.echo)



    def receive_initnode(self, payload):
        print "Miner received receive_initnode"
        pass

    def receive_msg(self, payload):
        print " received msg"
        Msg = ChainMsgProtrol.unpack(rlp.decode(payload))
        print "receive msg: %s"%Msg.msg














