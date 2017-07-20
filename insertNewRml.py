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
    c_Zzshhh = []
    c_update_id = []
    c_update_Lnid = []
    c_update_Zzshhhid = []
    jdeCursor.execute (" select trim(t.wwan8) as 客户,\
     t.WWIDLN as 行号\
     from proddta.f0111 t where 1=1 \
     and trim(t.wwan8) >5000000\
     and trim(t.wwan8)<5099999 \
     and t.WWIDLN <> 0\
     order by t.wwan8,t.WWIDLN")
    #5099999 and (trim(t.WWNTYP) = 4 or trim(t.WWNTYP) = 11)
    rows = jdeCursor.fetchall()
    for row in rows:
        oaCursor.execute("select id from uf_rml where C_ID = :1 and LNID = :2",(row[0],row[1]))
        temp = oaCursor.fetchone()
        if(temp is None):
            c_Id+=[row[0]]
            c_Lnid+=[row[1]]
            print row[0],
            print row[1]

    # for x in range(len(c_Zzshhh)):
    #     if(c_Zzshhh[x] is None):
    #         pass
    #     else:
    #         oaCursor.execute("select id from uf_rml where C_ID = :1 and LNID = :2",(c_Id[x],c_Zzshhh[x]))
    #         tempId = oaCursor.fetchone()
    #         if (tempId is None):
    #             print c_Id[x],
    #             print c_Lnid[x]
    #         else:
    #             c_update_id+=[c_Id[x]]
    #             c_update_Lnid+=[c_Lnid[x]]
    #             c_update_Zzshhhid+=[tempId[0]]

    # updateSql = "update uf_rml set ZZSHHH = :1 where C_ID = :2 and LNID = :3 "
    # updateParam = [[c_update_Zzshhhid[x]]+[c_update_id[x]]+[c_update_Lnid[x]] for x in range(len(c_update_id))]
    # oaCursor.executemany(updateSql,updateParam)
    # oaConn.commit()
    # print "Update Successfully"


except Exception as e:
    print e
    oaCursor.close()
    oaConn.close()
    print "OA Connection Disconnected_"
    jdeCursor.close()
    jdeConn.close()
    print "JDE Connection Disconnected_"
    raise




#关闭连接
jdeCursor.close()
jdeConn.close()
print "JDE Connection Disconnected"
oaCursor.close()
oaConn.close()
print "OA Connection Disconnected"
