#coding:utf-8
#!/usr/bin/python
import os
import time
import MySQLdb
import xlrd
import sys
import json
from datetime import date 
reload(sys)
sys.setdefaultencoding("utf-8")
#name={'媒体':'media','对应的推广地址':'site','对应地区':'addres','消费':'consume','点击':'click',\
#        '总有效量':'valide','总预约量':'appointment','总就诊量':'visit','当天无就诊量':'unvisit'}
def excel2mysql(fi):
    db = MySQLdb.connect("localhost","root","123","mysite",charset='utf8')
    cursor = db.cursor()
    l=[]
    z=[]
    t=[]
    wb=xlrd.open_workbook(fi,encoding_override="utf-8")
    wb.sheet_names()
    sh=wb.sheet_by_index(0)
    nrows=sh.nrows
    ncols=sh.ncols

    for row in range(0,nrows):
        t1=[]
        for col in range(0,ncols):
            if row==0:
                t.append(sh.cell(0,col).value)
            else:
                t1.append(sh.cell(row,col).value)
        if row>0:
            z.append(zip(t,t1))
    s=z
    try:
        for i in range(0,len(s)):
            r=cursor.execute('select * from opt_optimization where date(date) = curdate()')
            print r
            count=cursor.execute('select * from opt_optimization limit 0,%d'%r)
            t=cursor.fetchall()
            print "*****:%s"%count
            flag1=0
            if len(s[i])==9:
                sql="insert into opt_optimization values (null,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',null);\
                        "%(s[i][0][1],s[i][1][1],s[i][2][1],s[i][3][1],s[i][4][1],s[i][5][1],s[i][6][1],s[i][7][1],s[i][8][1])
            print sql
            if count >0:
                for j in  t:
                    if j[1] == s[i][0][1] and j[2] == s[i][1][1]  and j[3] == s[i][2][1] :
                                print "xxxxxx"
                                flag1=1
                    """if j[1] == s[i][0][1] and j[2] == s[i][1][1]  and j[3] == s[i][2][1] and j[4] == s[i][3][1]  and j[5] == s[i][4][1] \
                            and j[6] == s[i][5][1] and j[7] == s[i][6][1] and j[8] == s[i][7][1] and  j[9] == s[i][8][1] :
                                print "xxxxxx"
                                flag1=1"""

            if  count ==0 or flag1==0:
                try:
                    print "ooooo"
                    cursor.execute(sql)
                    db.commit()
                except Exception ,e:
                    print "error sql commit :%s"%e
                    db.rollback()
                    pass

    except Exception, e:
        print "error:%s"%e
        pass

    db.close()
def updateMysql():
    f='youhua_%s.xlsx'%date.today()
    print f
    if os.path.isfile('/home/btc/data/changjiang/%s'%f) :
        print "yyyy"
        excel2mysql('/home/btc/data/changjiang/%s'%f)
if __name__ == "__main__":
    while(1):
        updateMysql()
        time.sleep(10)
