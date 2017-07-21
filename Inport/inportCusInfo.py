# -*- coding: utf-8 -*-
import cx_Oracle
import os
import xlrd
import xlsxwriter
import sys
import datetime
import time
stdout = sys.stdout
stdin = sys.stdin
stderr = sys.stderr
reload( sys )
sys.setdefaultencoding('utf-8')
sys.stdout = stdout
sys.stdin = stdin
sys.stderr = stderr
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

oaConn = cx_Oracle.connect('oadb/oracle@192.168.0.89:1521/OADB')
oaCursor = oaConn.cursor()
print "OA Connection Connected"

def myConvertDateToStr(dateInput):
    if(type(dateInput) == unicode):
        dateStr = dateInput.encode("utf-8").strip()
        if(len(dateStr) != 10):
            print "Date Error:",
            print dateStr
        return dateStr
    if(type(dateInput) == float):
        dateTuple = xlrd.xldate_as_tuple(x,0)
        yearStr = str(dateTuple[0])
        if(dateTuple[1]<10):
            monStr = "0"+str(dateTuple[1])
        else:
            monStr = str(dateTuple[1])
        if(dateTuple[2] < 10):
            dayStr = "0"+str(dateTuple[2])
        else:
            dayStr = str(dateTuple[2])
        dateStr = yearStr+"-"+monStr+"-"+dayStr
        if(len(dateStr) == 10):
            return dateStr
        else:
            print "Date Error"
            print dateStr
            return ""

def myTrim(l):
    for x in range(len(l)):
        if type(l[x]) == float:
            if l[x]%1.0 == 0.0:
                l[x] = str(int(l[x]))
            else:
                print '第{}行{}错误'.format(x,l[0])
                l[x] = 'ERROR'
        l[x] = l[x].encode('utf-8').strip()
        if((l[x].find("　") != -1) or (l[x].find(" ") != -1)):
            print "第{}行{}存在空格".format(x,l[0])
            print l[x]

rawDataPath = 'C:\Users\jimmyyu\Desktop\excelInput\inputCus.xlsx'
rawDataBook = xlrd.open_workbook(rawDataPath)
rawSheet = rawDataBook.sheet_by_index(0)
codeList = rawSheet.col_values(0)[1:]
addressList = rawSheet.col_values(4)[1:]
clnfList_ = rawSheet.col_values(5)[1:]
xydmList = rawSheet.col_values(6)[1:]
zczjList = rawSheet.col_values(7)[1:]
dqrList_ =  rawSheet.col_values(9)[1:]
clnfList = []
dqrList = []
myTrim(codeList)
myTrim(addressList)
myTrim(xydmList)
myTrim(zczjList)
for x in clnfList_:
    if(type(x)==float):
        clnfList+=[xlrd.xldate_as_tuple(x,0)[0]]
    else:
        clnfList+=['']
for x in dqrList_:
    if(type(x)==float):
        dqrList+=[myConvertDateToStr(x)]
    else:
        dqrList+=['']


try:
    for x in range(len(codeList)):
        eachUpdateSql = "update uf_customers set C_REGADDRESS = \'{}\',\
C_FOUNDYEAR=\'{}\',C_CREDITCODE=\'{}\',C_REGFUND=\'{}\',C_EXPDATE=\'{}\' where \
C_ID = {}".format(addressList[x],clnfList[x],xydmList[x],zczjList[x],dqrList[x],codeList[x])
        print eachUpdateSql
        oaCursor.execute(eachUpdateSql)
    oaConn.commit()

except Exception as e:
    print e
    oaCursor.close()
    oaConn.close()
    print "OA Connection Disconnected_"
    raise


oaCursor.close()
oaConn.close()
print "OA Connection Disconnected"
