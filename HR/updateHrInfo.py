# -*- coding: utf-8 -*-
import xlrd
import xlsxwriter
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

dbConn = True
hrInputPath = 'D:\Work\OA\hrFile\hrInput.xlsx'
#############工具函数#####################
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

def myLookUp(value,targetList,valueCol,targetCol):
    for eachRow in targetList:
        if(eachRow[valueCol] == value):
            return eachRow[targetCol]
    print str(value)+" Not Found"
    return ""

#################################################
if(dbConn):
    jdeConn = cx_Oracle.connect('jdetest/jdetest@192.168.0.238:1521/E1DB')
    jdeCursor = jdeConn.cursor()
    print "JDE Connection Connected"
    oaConn = cx_Oracle.connect('oadb/oracle@192.168.0.89:1521/OADB')
    oaCursor = oaConn.cursor()
    print "OA Connection Connected"

def mySelect(paraList,tableName,cursorName):
    paraStr = ",".join(paraList)
    cursorName.execute("select "+paraStr+" from "+tableName)
    return cursorName.fetchall()

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


try:
    locationList = mySelect(["id","locationname"],"HrmLocations",oaCursor)
    zzList = mySelect(["udc","val"],"edi.v_wf_udc_org",jdeCursor)
    qyList = mySelect(["udc","val"],"edi.v_wf_udc_area",jdeCursor)
    tixiList = [(0,"业务体系"),(1,"运作体系")]
    sexList = [(0,"男"),(1,"女")]
    # result = myLookUp("上海",locationList,1,0)

    #打开excel获取数据
    hrInputBook = xlrd.open_workbook(hrInputPath)
    inputSheet = hrInputBook.sheet_by_index(0)

    workcode = inputSheet.col_values(0)[1:]
    names = inputSheet.col_values(1)[1:]
    engNames = inputSheet.col_values(2)[1:]
    workLocations_ = inputSheet.col_values(3)[1:]
    zz_ = inputSheet.col_values(4)[1:]
    myTrim(zz_)
    zz = [myLookUp(x,zzList,1,0) for x in zz_]
    qy_ = inputSheet.col_values(5)[1:]
    myTrim(qy_)
    qy = [myLookUp(x,qyList,1,0) for x in qy_]
    tixi_ = inputSheet.col_values(6)[1:]
    myTrim(tixi_)
    tixi = [myLookUp(x,tixiList,1,0) for x in tixi_]
    sfz = inputSheet.col_values(14)[1:]
    birthday_ = inputSheet.col_values(15)[1:]
    birthday = [myConvertDateToStr(x) for x in birthday_]
    sex_ = inputSheet.col_values(17)[1:]
    myTrim(sex_)
    sex = [myLookUp(x,sexList,1,0) for x in sex_]
    rzDate_ = inputSheet.col_values(18)[1:]
    ygType_ = inputSheet.col_values(19)[1:]

    for x in zz:
        print x
    for x in qy:
        print x
    for x in tixi:
        print x
    for x in birthday:
        print x
    for x in sex:
        print x
    # myTrim(workcode)
    # myTrim(names)
    # for x in workcode:
    #     print x,
    #     print type(x)
    # for x in names:
    #     print x,
    #     print type(x)

    #查询语句
    # oaCursor.execute('select t.workcode,t.lastname from hrmresource@oatest t where id = 89')
    # rows = oaCursor.fetchall()
    # for row in rows:
    #     for x in row:
    #         print x,
    #         print type(x)


    #更新语句
    # updateSql = "update hrmresource@oatest set lastname = :1 where workcode = :2"
    # updateParam = [[names[x]]+[workcode[x]] for x in range(len(workcode))]
    # oaCursor.executemany(updateSql,updateParam)
    # oaConn.commit()



except Exception as e:
    print e
    if(dbConn):
        jdeCursor.close()
        jdeConn.close()
        print "JDE Connection Disconnected"
        oaCursor.close()
        oaConn.close()
        print "OA Connection Disconnected_"
    raise

#关闭连接
if(dbConn):
    jdeCursor.close()
    jdeConn.close()
    print "JDE Connection Disconnected"
    oaCursor.close()
    oaConn.close()
    print "OA Connection Disconnected"
