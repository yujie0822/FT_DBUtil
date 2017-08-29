# -*- coding: utf-8 -*-
import cx_Oracle
import SqlEnv

oaConn = cx_Oracle.connect(SqlEnv.MAIN_OA_CONNECT_STRING)
oaCursor = oaConn.cursor()
print "OA Connection Connected"

try:
    p1=12345
    msg = oaCursor.var(cx_Oracle.STRING)
    oaCursor.callproc('P_TEST_JIMMY',[p1,msg])

    print msg.getvalue()

except Exception as e:
    print e
    oaCursor.close()
    oaConn.close()
    print "OA Connection Disconnected"
    raise


#关闭连接
oaCursor.close()
oaConn.close()
print "OA Connection Disconnected"
