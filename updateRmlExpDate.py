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
    c_ExpDate = []
    jdeCursor.execute (" select trim(t.wwan8) as 客户,\
     t.WWIDLN as 行号,\
     trim(t.WWNTYP) as 联系人类型,\
     trim(WWDYR) as year,\
     trim(WWDMON) as mon,\
     trim(WWDDATE) as day\
     from proddta.f0111 t where 1=1  \
     and trim(t.wwan8) >5000000\
     and trim(t.wwan8)<5099999 \
     order by t.wwan8,t.WWIDLN")
    #5099999 and (trim(t.WWNTYP) = 4 or trim(t.WWNTYP) = 11)
    rows = jdeCursor.fetchall()
    for row in rows:
        c_Id+=[row[0]]
        c_Lnid+=[row[1]]
        c_date = ''
        if(int(row[3])<=0):
            pass
        elif(len(row[3])==2):
            c_date+='20'+str(row[3])
        elif(len(row[3])==4):
            c_date+=str(row[3])
        if(len(c_date)==4):
            for x in range(2):
                if(int(row[x+4]) <= 0):
                    pass
                else:
                    c_date+="-"
                    if(int(row[x+4])<10):
                        c_date+='0'+str(row[x+4])
                    else:
                        c_date+=str(row[x+4])


        if(len(c_date)==10 or len(c_date)==0):
            c_ExpDate+=[c_date]
        else:
            c_ExpDate+=[""]
            print c_date,
            print ",",
            print row[0],
            print ",",
            print row[1]


    updateSql = "update uf_rml set EXPDATE = :1 where C_ID = :2 and LNID = :3 "
    updateParam = [[c_ExpDate[x]]+[c_Id[x]]+[c_Lnid[x]] for x in range(len(c_Id))]
    oaCursor.executemany(updateSql,updateParam)
    oaConn.commit()
    print "Update Successfully"


except Exception as e:
    print e
    oaCursor.close()
    oaConn.close()
    print "OA Connection Disconnected"
    jdeCursor.close()
    jdeConn.close()
    print "JDE Connection Disconnected"
    raise




#关闭连接
jdeCursor.close()
jdeConn.close()
print "JDE Connection Disconnected"
oaCursor.close()
oaConn.close()
print "OA Connection Disconnected"
