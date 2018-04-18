# coding:utf8

import sys
sys.path.append("..")

from Network.MinerNode import MinerNode
from Network.protrol import *
import traceback
import time

try:
    # address, udpPort, tcpPort
    myendpoint = EndPoint(u'127.0.0.1', 30307, 30308)
    Discoverpoint = EndPoint(u'127.0.0.1', 30303, 30304)

    miner = MinerNode(myendpoint)

    # udp listern
    miner.start_udp_listern()

    print 'start tcp server '
    # tcp listern
    miner.start_tcp_listern()

    print 'start ping server'

    # ping发现节点
    miner.ping(Discoverpoint)
    while True:
        time.sleep(600)

except:
    traceback.print_exc()
    sys.exit(1)





