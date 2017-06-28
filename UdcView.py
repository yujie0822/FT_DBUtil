# -*- coding: utf-8 -*-
import cx_Oracle
import sys
from DBUtils.PooledDB import PooledDB
stdout = sys.stdout
stdin = sys.stdin
stderr = sys.stderr
reload( sys )
sys.setdefaultencoding('utf-8')
sys.stdout = stdout
sys.stdin = stdin
sys.stderr = stderr

class Jde(object):
    #连接池对象
    __pool = None

    def __init__(self):
        try:
            self._conn = cx_Oracle.connect('jdetest/jdetest@192.168.0.238:1521/E1DB')
            self._cursor = self._conn.cursor()
            print "Connected"
        except Exception,e:
            print 'Connect failed! Error{}.{}'.format(e.args[0],e.args[1])
            sys.exit()


    @staticmethod


    def getPlineView(self):
        """
        @summary：查询产品线视图
        @return：result list [[UDC1,Pline1],[UDC2,Pline2],......]
        """
        self._cursor.execute ("select * from edi.v_wf_udc_pline")
        row = self._cursor.fetchall()
        return row



    def dispose(self):
        self._cursor.close()
        self._conn.close()
        print "Disconnected to Database"

    def __del__(self):
        self._cursor.close()
        self._conn.close()
        print "Disconnected to Database"
