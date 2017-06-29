# -*- coding: utf-8 -*-
import cx_Oracle
import os
import sys
stdout = sys.stdout
stdin = sys.stdin
stderr = sys.stderr
reload( sys )
sys.setdefaultencoding('utf-8')
sys.stdout = stdout
sys.stdin = stdin
sys.stderr = stderr
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

jdeConn = cx_Oracle.connect('jdetest/jdetest@192.168.0.238:1521/E1DB')
jdeCursor = jdeConn.cursor()
print "JDE Connection Connected"

oaConn = cx_Oracle.connect('oadb/oracle@192.168.0.89:1521/OADB')
oaCursor = oaConn.cursor()
print "OA Connection Connected"

try:
    c_Id = []
    c_Lnid = []
    c_Address = []
    c_HyFkName = []
    jdeCursor.execute (" select trim(t.wwan8) as 客户,\
     t.WWIDLN as 行号,\
     trim(t.WWNTYP) as 联系人类型,\
     trim(t.WWATTL) as 地址1, \
     trim(t.WWREM1) as 地址2, \
     trim(t.WWNICK) as 地址3, \
     trim(t.WWGNNM) as 地址4, \
     trim(t.WWSRNM) as 地址5, \
     trim(t.WWSLNM) as 地址6 \
     from proddta.f0111 t where (trim(t.WWNTYP) = 4 or trim(t.WWNTYP) = 11) \
     and trim(t.wwan8) >5000000\
     and trim(t.wwan8)<5099999 \
     order by t.wwan8,t.WWIDLN")
    rows = jdeCursor.fetchall()
    for row in rows:
        c_Id+=[row[0]]
        c_Lnid+=[row[1]]
        c_Add = ''
        c_name = ''
        for x in range(2):
            if(row[x+3] is None):
                pass
            else:
                c_name+=row[x+3]
        for x in range(4):
            if(row[x+5] is None):
                pass
            else:
                c_Add+=row[x+5]
        c_HyFkName+=[c_name]
        c_Address+=[c_Add]

    updateSql = "update uf_rml set HY_FK_NAME = :1 ,C_ADDRESS = :2 where C_ID = :3 and LNID = :4 "
    updateParam = [[c_HyFkName[x]]+[c_Address[x]]+[c_Id[x]]+[c_Lnid[x]] for x in range(len(c_Id))]
    oaCursor.executemany(updateSql,updateParam)
    oaConn.commit()
    print "Update Successfully"


except Exception as e:
    print e
    oaCursor.close ()
    oaConn.close ()
    print "OA Connection Disconnected"
    jdeCursor.close()
    jdeConn.close()
    print "JDE Connection Disconnected"
    raise




#关闭连接
jdeCursor.close()
jdeConn.close()
print "JDE Connection Disconnected"
oaCursor.close ()
oaConn.close ()
print "OA Connection Disconnected"
