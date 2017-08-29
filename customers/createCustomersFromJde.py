# -*- coding: utf-8 -*-
import cx_Oracle
import os
import sys
import datetime
stdout = sys.stdout
stdin = sys.stdin
stderr = sys.stderr
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdout = stdout
sys.stdin = stdin
sys.stderr = stderr
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

now=datetime.datetime.now()
date_today = now.strftime('%Y-%m-%d')
time_now = now.strftime('%H:%M:%S')

jdeConn = cx_Oracle.connect('jdetest/jdetest@192.168.0.238:1521/E1DB')
jdeCursor = jdeConn.cursor()
print "JDE Connection Connected"

oaConn = cx_Oracle.connect('oadb/oracle@192.168.0.89:1521/OADB')
oaCursor = oaConn.cursor()
print "OA Connection Connected"

startAn8 = "5010037"
endAn8 = "5999999"

try:
    jdeCursor.execute("select t2.C_ID,t2.C_NAME,t2.C_AREA,t2.AICUSTS,t2.KHTYPE,\
t2.BCXY,t2.YYLY,t2.JCKQ,t2.FKFS,t2.KAIPIAODIZHI,t2.KAIPIAODIANHUA,\
t2.KAIHUYINHANG,t2.YINHANGZHANGHAO,t2.SHUIHAO from jdetest.V_WF_khbase t2 \
where t2.C_ID>="+startAn8+" and t2.C_ID <="+endAn8+"  order by t2.C_ID")

    jdeCustomersRows = jdeCursor.fetchall()

#   5000000  5009000
    oaCursor.execute("select t.C_ID,t.C_NAME from uf_customers t \
    where C_ID>="+startAn8+" and C_ID <="+endAn8+" order by C_ID")
    oaCustomersRows = oaCursor.fetchall()

    oaCustomersId = []
    for eachOaCustomers in oaCustomersRows:
        oaCustomersId+=[int(eachOaCustomers[0])]

    for eachJdeCustomers in jdeCustomersRows:
        if (int(eachJdeCustomers[0]) not in oaCustomersId):
            tempList = list(eachJdeCustomers)
            for x in range(len(tempList)):
                if(tempList[x] is None):
                    tempList[x] = ''
                else:
                    tempList[x] = str(tempList[x])
            insertSql = "insert into uf_customers (C_ID,C_NAME,C_AREA,C_STATUS,khjyzt,\
bcxy,C_APPLYFIELD,khjckq,kpdz,dh,khyh,yhzh,sh,C_CONTRACT,C_ISNCNR,FORMMODEID,\
MODEDATACREATER,MODEDATACREATERTYPE,MODEDATACREATEDATE,MODEDATACREATETIME) VALUES \
(\'"+tempList[0]+"\',\'"+tempList[1]+"\',\'"+tempList[2]+"\',\'"\
            +tempList[3]+"\',\'"+tempList[4]+"\',\'"+tempList[5]+"\',\'"\
            +tempList[6]+"\',\'"+tempList[7]+"\',\'"\
            +tempList[9]+"\',\'"+tempList[10]+"\',\'"+tempList[11]+"\',\'"\
            +tempList[12]+"\',\'"+tempList[13]+"\',0,0,3,89,0,\'"+date_today\
            +"\',\'"+time_now+"\')"

            print "insert:"+tempList[0]

            oaCursor.execute(insertSql)

            insertZqSql = "insert INTO uf_khzq (C_ID,FORMMODEID,MODEDATACREATER,\
MODEDATACREATERTYPE,MODEDATACREATEDATE,MODEDATACREATETIME) VALUES ({},341,89,0\
,\'{}\',\'{}\')".format(tempList[0],date_today,time_now)

            oaCursor.execute(insertZqSql)
            oaCursor.callproc('p_cus_addqx',[tempList[0]])
    oaConn.commit()

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
