
import leveldb

class DBService(object):

    def __init__(self, dataname):
        self._db = leveldb.LevelDB(dataname)

    def clear_db(self):
        b = leveldb.WriteBatch()
        for k in self._db.RangeIter(include_value=False, reverse=True):
            b.Delete(k)
        self._db.Write(b)

    def insert_db(self, object_list):
        b = leveldb.WriteBatch()
        for (k, v) in object_list:
            b.Put(k, v)
        self._db.Write(b)

    def getAllChainMsg(self):
        res = []
        for key, value in self._db.RangeIter():
            res.append((key, value))
        return res

    def insert(self, sid, name):
        self._db.Put(str(sid), name)

    def delete(self, sid):
        self._db.Delete(str(sid))

    def update(self, sid, name):
        self._db.Put(str(sid), name)

    def search(self, sid):
        name = self._db.Get(str(sid))
        return name





















