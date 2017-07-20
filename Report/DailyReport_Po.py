# -*- coding: utf-8 -*-
import cx_Oracle
import os
import sys
import datetime
import smtplib
import math
from email.mime.text import MIMEText
stdout = sys.stdout
stdin = sys.stdin
stderr = sys.stderr
reload( sys )
sys.setdefaultencoding('utf-8')
sys.stdout = stdout
sys.stdin = stdin
sys.stderr = stderr
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

now=datetime.datetime.now()
yesterday = now+datetime.timedelta(days=-1)
date_today = now.strftime('%Y-%m-%d')
time_now = now.strftime('%H:%M:%S')
date_yesterday = yesterday.strftime('%Y-%m-%d')
date_yesterdayList = [yesterday.month,yesterday.day]

oaConn = cx_Oracle.connect('oadb/oracle@192.168.0.89:1521/OADB')
oaCursor = oaConn.cursor()
print "OA Connection Connected"


def findListNotInList(l1,l2):
    l3 = []
    for x in l1:
        if x not in l2:
            l3+=[x]
    return l3

def createReportSql(wfid,dateFromStr,dateToStr):
    resultStr = "select t_req.requestid,t_req.currentnodeid from workflow_requestbase \
t_req left join workflow_nodebase t_node on t_node.id = t_req.currentnodeid \
where t_req.workflowid = "+str(wfid)+" and t_req.createdate >= \'"+dateFromStr+"\'\
and t_req.createdate <= \'"+dateToStr+"\'"
    return resultStr

def createPersonalReportSql(userid,wfid,dateFromStr1,dateToStr1,dateFromStr2,dateToStr2):
    resultStr = """
(select count(t_ope.requestid) from workflow_currentoperator t_ope
left join workflow_requestbase t_req on t_req.requestid = t_ope.requestid
where t_ope.userid = {0} and t_ope.workflowid = {1} and t_req.createdate >= '{2}' and t_req.createdate <= '{3}')
union
(select count(t_ope.requestid) from workflow_currentoperator t_ope
left join workflow_requestbase t_req on t_req.requestid = t_ope.requestid
where t_ope.userid = {0} and t_ope.workflowid = {1} and t_req.createdate >= '{4}' and t_req.createdate <= '{5}')
""".format(userid,wfid,dateFromStr1,dateToStr1,dateFromStr2,dateToStr2)
    return resultStr
try:
    print createReportSql(182,date_yesterday,date_yesterday)
    # 今日采购订单节点状态List
    oaCursor.execute(createReportSql(182,date_yesterday,date_yesterday))
    poTodayStatus = oaCursor.fetchall()
    poTodayNodes = [x[1] for x in poTodayStatus]
    poCol = [0 for x in range(9)]
    #MC
    poCol[0] = poTodayNodes.count(742)
    #PLM
    poCol[1] = poTodayNodes.count(743)
    #PLD
    poCol[2] = poTodayNodes.count(744)
    #Frank
    poCol[3] = poTodayNodes.count(1141)
    #Segment负责人
    poCol[4] = poTodayNodes.count(745)
    #董事长
    poCol[5] = poTodayNodes.count(746)
    #物控经理盖章
    poCol[6] = poTodayNodes.count(748)
    # 流程结束
    poCol[7] = poTodayNodes.count(749)+poTodayNodes.count(747)
    #总计
    poCol[8] = len(poTodayNodes)-poTodayNodes.count(750)

    percentCol = [int(round(float(poCol[x])*100.0/float(poCol[8]))) for x in range(9)]

    # 累计采购订单节点状态List
    oaCursor.execute(createReportSql(182,'2017-07-01',date_yesterday))
    poAllStatus = oaCursor.fetchall()
    poAllNodes = [x[1] for x in poAllStatus]
    poCol_t = [0 for x in range(9)]
    #MC
    poCol_t[0] = poAllNodes.count(742)
    #PLM
    poCol_t[1] = poAllNodes.count(743)
    #PLD
    poCol_t[2] = poAllNodes.count(744)
    #Frank
    poCol_t[3] = poAllNodes.count(1141)
    #Segment负责人
    poCol_t[4] = poAllNodes.count(745)
    #董事长
    poCol_t[5] = poAllNodes.count(746)
    #物控经理盖章
    poCol_t[6] = poAllNodes.count(748)
    # 流程结束
    poCol_t[7] = poAllNodes.count(749)+poAllNodes.count(747)
    #总计
    poCol_t[8] = len(poAllNodes)-poAllNodes.count(750)

    percentCol_t = [int(round(float(poCol_t[x])*100.0/float(poCol_t[8]))) for x in range(9)]

    oaCursor.execute(createPersonalReportSql(21,182,date_yesterday,date_yesterday,'2017-07-10',date_yesterday))
    lawStatus = oaCursor.fetchall()
    law_total_today = lawStatus[0][0]
    law_total_all = lawStatus[1][0]

    #节点异常处理
    otherNodeList = findListNotInList(poTodayNodes,[742,743,744,1141,745,746,748,749,747,750])
    otherNodeList_t = findListNotInList(poAllNodes,[742,743,744,1141,745,746,748,749,747,750])

    if(len(otherNodeList)!=0):
        print otherNodeList
    if(len(otherNodeList_t)!=0):
        print otherNodeList_t

    #--------------------发送Email部分-------------------------
    sender = 'jimmyyu@fortune-co.com'
    receiver = ['ERPSUPPORT@fortune-co.com','jacksun@fortune-co.com']
    subject = str(now.month)+'月'+str(now.day-1)+'日销售订单审批流程试运行总结'
    smtpserver = 'smtp.fortune-co.com'
    username = 'jimmyyu@fortune-co.com'
    password = 'Xiaoyu822'

    htmlContent = """
<html>
<head>
  <style media="screen">
    .myHead{
      padding: 5px 5px 10px 10px;
    }
    .myText{
      padding: 5px 10px 0px 30px;
    }
    .myTableRow{
      padding: 10px 0px 5px 5px;
    }
    .myTable{
      border-collapse:collapse;
    }
    .myTable th,td{
      border: 1px solid black;
      padding:3px 7px 2px 7px;
    }

  </style>
</head>
"""+"""
<body>
  <div>
    <h2 class="myHead">OA流程节点统计日报表</h2>
  </div>
  <div class="myText">
    <p>以下分别列出{date[0]}月{date[1]}日当日及截止{date[0]}月{date[1]}日累计采购订单审批流程试运行的情况：</p>
    <p>{date[0]}月{date[1]}日当日：</p>
    <ol>
      <li>今天的有效订单一共{l1[8]}单，流程结束的一共{l1[7]}单，批到Lawrence的{law_total_today}单
        -总占比{law_total_today_p}%</li>
      <li>流程各节点占比情况:
        <div class="myTableRow">
          <table class="myTable">
            <tr>
              <th>节点</th>
              <th>数量</th>
              <th>占比</th>
            </tr>
            <tr>
              <td>MC</td>
              <td>{l1[0]}</td>
              <td>{l2[0]}%</td>
            </tr>
            <tr>
              <td>产品线经理</td>
              <td>{l1[1]}</td>
              <td>{l2[1]}%</td>
            </tr>
            <tr>
              <td>产品线总监</td>
              <td>{l1[2]}</td>
              <td>{l2[2]}%</td>
            </tr>
            <tr>
              <td>运作副总</td>
              <td>{l1[3]}</td>
              <td>{l2[3]}%</td>
            </tr>
            <tr>
              <td>Segment负责人</td>
              <td>{l1[4]}</td>
              <td>{l2[4]}%</td>
            </tr>
            <tr>
              <td>董事长</td>
              <td>{l1[5]}</td>
              <td>{l2[5]}%</td>
            </tr>
            <tr>
              <td>物控经理盖章</td>
              <td>{l1[6]}</td>
              <td>{l2[6]}%</td>
            </tr>
            <tr>
              <td>流程结束</td>
              <td>{l1[7]}</td>
              <td>{l2[7]}%</td>
            </tr>
            <tr>
              <th>总计</th>
              <td>{l1[8]}</td>
              <td>{l2[8]}%</td>
            </tr>
          </table>
        </div>
      </li>
    </ol>
    <p>截止{date[0]}月{date[1]}日累计：</p>
    <ol>
      <li>累计的有效订单一共{l1_t[8]}单，流程结束的一共{l1_t[7]}单，
        批到Lawrence的{law_total_all}单-总占比{law_total_all_p}%</li>
        <li>流程各节点占比情况:
          <div class="myTableRow">
            <table class="myTable">
              <tr>
                <th>节点</th>
                <th>数量</th>
                <th>占比</th>
              </tr>
              <tr>
                <td>MC</td>
                <td>{l1_t[0]}</td>
                <td>{l2_t[0]}%</td>
              </tr>
              <tr>
                <td>产品线经理</td>
                <td>{l1_t[1]}</td>
                <td>{l2_t[1]}%</td>
              </tr>
              <tr>
                <td>产品线总监</td>
                <td>{l1_t[2]}</td>
                <td>{l2_t[2]}%</td>
              </tr>
              <tr>
                <td>运作副总</td>
                <td>{l1_t[3]}</td>
                <td>{l2_t[3]}%</td>
              </tr>
              <tr>
                <td>Segment负责人</td>
                <td>{l1_t[4]}</td>
                <td>{l2_t[4]}%</td>
              </tr>
              <tr>
                <td>董事长</td>
                <td>{l1_t[5]}</td>
                <td>{l2_t[5]}%</td>
              </tr>
              <tr>
                <td>物控经理盖章</td>
                <td>{l1_t[6]}</td>
                <td>{l2_t[6]}%</td>
              </tr>
              <tr>
                <td>流程结束</td>
                <td>{l1_t[7]}</td>
                <td>{l2_t[7]}%</td>
              </tr>
              <tr>
                <th>总计</th>
                <td>{l1_t[8]}</td>
                <td>{l2_t[8]}%</td>
              </tr>
            </table>
          </div>
        </li>
    </ol>
  </div>
</body>
</html>

""".format(date=date_yesterdayList,l1=poCol,l2=percentCol,\
l1_t=poCol_t,l2_t=percentCol_t,\
law_total_today=law_total_today,law_total_today_p=int(round(law_total_today*100.0/poCol[7]+poCol[6])),\
law_total_all=law_total_all,law_total_all_p=int(round(law_total_all*100.0/poCol_t[7]+poCol_t[6])),\
)

    msg = MIMEText(htmlContent,'html','utf-8')
    msg['Subject'] = subject
    msg['from'] = 'jimmyyu@fortune-co.com'
    msg['to'] = ','.join(receiver)
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print "邮件发送成功"

except Exception as e:
    print e
    oaCursor.close()
    oaConn.close()
    print "OA Connection Disconnected_"
    raise

#关闭连接
oaCursor.close()
oaConn.close()
print "OA Connection Disconnected"
