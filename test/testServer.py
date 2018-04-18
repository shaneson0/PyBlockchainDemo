# coding:utf8

import sys
sys.path.append("..")
from Network.DiscoverNode import DiscoverNode
from Network.protrol import *
import sys
import traceback
import time

try:
    ServeriPoint = EndPoint(u'127.0.0.1', 30303, 30304)
    server = DiscoverNode(endpoint=ServeriPoint)
    # udp listern
    server.start_udp_listern()
    while True:
        time.sleep(600)
except:
    traceback.print_exc()
    print 'sys exit'
    sys.exit(1)





# Serverendpoint = EndPoint(u'192.168.0.100', 30303, 30303)
#
# # 引导节点
# Bob_endpoint = EndPoint(u'13.93.211.84', 30303, 30303)
#
#
# server = PingServer(my_endpoint=Serverendpoint)
# listern_thread = server.udp_listen()
# listern_thread.start()
#
#
# server.ping(Bob_endpoint)



