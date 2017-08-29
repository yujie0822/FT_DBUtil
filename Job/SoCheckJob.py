# -*- coding: utf-8 -*-
import cx_Oracle,sys,datetime,smtplib,math
sys.path.append(".")
import SqlEnv,MailUtil,JobLog

oaConn = cx_Oracle.connect(SqlEnv.MAIN_OA_CONNECT_STRING)
oaCursor = oaConn.cursor()
JobLog.logger.debug("销售订单表单检查：OA Database Connected")

mailText = ""
mailTag = False
try:
    oaCursor.execute("""(select t1.requestid,t2.currentnodeid
from formtable_main_11 t1
left join workflow_requestbase t2 on t1.requestid=t2.requestid
where t2.currentnodeid <> 261 and t1.bm is null )
union
(select t1.requestid,t2.currentnodeid
from formtable_main_15 t1
left join workflow_requestbase t2 on t1.requestid=t2.requestid
where t2.currentnodeid <> 270 and t1.bm is null )
""")
    rows = oaCursor.fetchall()
    if(len(rows)>0):
        mailTag=True
        for row in rows:
            mailText+=str(row[0])+" "
        mailText+="流程无部门\n"

    if mailTag:
        MailUtil.sendTextMailTo(["jimmyyu@fortune-co.com"],"销售订单表单检查",mailText)

except Exception as e:
    JobLog.logger.error("销售订单表单检查：%s".format(e),exc_info=True)
    raise

finally:
    oaCursor.close()
    oaConn.close()
    JobLog.logger.debug("销售订单表单检查：OA Database Disconnected")
