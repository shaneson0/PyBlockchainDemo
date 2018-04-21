
import sys
sys.path.append("../../")

from Service import DBServeice



database = DBServeice.DBService('test')
objectlist = [{"a": "b"}]
database.insert_db(objectlist)

res = database.getAllChainMsg()
print res

