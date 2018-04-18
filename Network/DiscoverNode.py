# -*- coding: utf8 -*-



import random
from P2PNetwork import PingServer
from protrol import *

# 发现节点
# 发现节点的功能主要是，发现周围的节点，并且随机提供一个节点给连接节点进行P2P连接
# DiscoverNode本身也是一个节点,所以构造函数需要把当前节点假如nodelist
# 端口默认暴露30303


class DiscoverNode(PingServer):
    def __init__(self, endpoint):
        self.nodelist = []
        super(DiscoverNode, self).__init__(endpoint)

    # 重载父类的receive_ping方法
    # pong回给连接节点，提示收到ping
    def receive_ping(self, payload):
        print " received in DiscoverNode"
        pingNode = PingProtrol.unpack(rlp.decode(payload))
        try:
            connectNodeMsg = self.getNodeMsg()
            pongNode = PongProtrol(pingNode.endpoint_from, connectNodeMsg, time.time())
            print 'nodelist is ok '
        except:
            print 'nodelist is null '
            pongNode = InitNodeProtrol(pingNode.endpoint_from, u'', time.time())
        self.pong(pongNode)

        # 在节点列表中注册
        self.register(pingNode.endpoint_from)

    def getNodeMsg(self):
        if len(self.nodelist) == 0:
            raise Exception
        nodemsg = random.sample(self.nodelist, 1)
        return nodemsg[0]

    def register(self, endpoint_from):
        self.nodelist.append(self.SpecialEncode(endpoint_from))

    def leave(self, endpoint):
        self.nodelist.remove(endpoint)






