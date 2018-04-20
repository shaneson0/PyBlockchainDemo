# coding:utf8

import leveldb
import os, sys

_db = None

def initialize(nodeid):
    _db = leveldb.LevelDB(nodeid)
    return _db

def insert(sid, name):
    _db.Put(str(sid), name)

def delete(sid):
    _db.Delete(str(sid))

def update(sid, name):
    _db.Put(str(sid), name)

def search(sid):
    name = _db.Get(str(sid))
    return name

def getAllChainMsg():
    res = []
    for key, value in _db.RangeIter():
        res.append((key,value))
    return res






