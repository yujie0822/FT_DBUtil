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

rawDataPath = 'C:\Users\jimmyyu\Desktop\excelInput\inputZq.xlsx'
rawDataBook = xlrd.open_workbook(rawDataPath)
rawSheet = rawDataBook.sheet_by_index(0)
codeList = rawSheet.col_values(0)[1:]
infoList = rawSheet.col_values(1)[1:]
myTrim(infoList)
for x in range(len(codeList)):
    print infoList[x][(infoList[x].find("*")+1):]
