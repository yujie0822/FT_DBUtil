# -*- coding: utf-8 -*-
from OadbUtil import Ora
db_info_oa = {'dbtype':'oracle','user':'OADB','pwd':'oracle',\
'host':'192.168.0.89','port':'1521','db':'OADB'}

db_info_jde = {'dbtype':'oracle','user':'jdetest','pwd':'jdetest',\
'host':'192.168.0.238','port':'1521','db':'E1DB'}
#
oaDb = Ora(db_info = db_info_oa)
rows = oaDb.query("select * from hrmresource where id = 89")
for x in rows:
    for y in x:
        print y


jdeDb = Ora(db_info = db_info_jde)
rows2 = jdeDb.query("select * from edi.v_wf_udc_pline")
for x in rows2:
    for y in x:
        print y

rows3 = oaDb.query("select * from hrmresource where id = 41")

print rows3
