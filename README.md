# PyBlockchainDemo



-------------------------
搭建p2p网络层，使用leveldb持久化。
难点：
1. p2p网络
2. 共识机制
3. 工作量证明算法（POW）

-------------

2018/04/18

完成P2P网络的搭建，P2P网络分为两层
1. 发现节点服务
2. 矿工网络层

协议层有两层
第一层是udp实现的发现协议，请求到发现节点服务获得p2p直连的节点；
第二层是tcp实现的连接协议，用于点对点服务和Chain服务

协议参考了以太坊的实现方式：
hash || signature || packet-type || packet-data

使用私钥对数据包进行签名，使用keccak-256对数据进行hash。

---------------

服务列表

services = [
    DBService,
    AccountsService,
    NodeDiscovery,
    PeerManager,
    ChainService,
    PoWService,
    JSONRPCServer]
