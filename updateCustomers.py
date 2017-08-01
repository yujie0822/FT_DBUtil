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
