# -*- coding: utf-8 -*-
from OadbUtil import Ora
db_info_oa = {'dbtype':'oracle','user':'OADB','pwd':'oracle',\
'host':'192.168.0.89','port':'1521','db':'OADB'}

db_info_jde = {'dbtype':'oracle','user':'jdetest','pwd':'jdetest',\
'host':'192.168.0.238','port':'1521','db':'E1DB'}

oaDb = Ora(db_info = db_info_oa)
oaDb.update('uf_rml',{'NAME_CN':'123'},{'C_ID':5005560,'LNID':3})
oaDb.commit()
# rows = oaDb.query("select * from hrmresource where id = 89")
# for x in rows:
#     for y in x:
#         print y
"""
def isCN(inputStr):
    count = 0;
    for x in inputStr:
        if ord(x)>10000:
            count+=1
    if(count>(len(inputStr)/3)):
        return True
    else:
        return False

jdeDb = Ora(db_info = db_info_jde)
rows2 = jdeDb.query(" select trim(t.wwan8) as 客户,\
 t.WWIDLN as 行号,\
 trim(t.WWNTYP) as 联系人类型,\
 trim(t.WWATTL) as 地址1, \
 trim(t.WWREM1) as 地址2, \
 trim(t.WWNICK) as 地址3, \
 trim(t.WWGNNM) as 地址4, \
 trim(t.WWSRNM) as 地址5, \
 trim(t.WWSLNM) as 地址6 \
 from proddta.f0111 t where trim(t.WWNTYP) <> 4 and trim(t.WWNTYP) <> 11 \
 and trim(t.wwan8) in (5000038,5000025)\
 --and trim(t.wwan8)<5000002 \
 order by t.wwan8,t.WWIDLN")
for x in rows2:
    if x[3] is None:
        pass
    else:
        print x[3]
        if(isCN(x[3])):
            print "是中文"
        else:
            print "是英文"

"""



# rows3 = oaDb.query("select * from hrmresource where id = 41")
#
# print rows3
