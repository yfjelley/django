#coding:utf-8
#!/usr/bin/python
import os,datetime,time,MySQLdb,xlrd,sys,json,glob
from time import localtime
from datetime import date
reload(sys).setdefaultencoding("utf-8")

def excel2mysql(fi):
    date_test=fi.split("_")[1].split(".")[0]
    print date_test
    db = MySQLdb.connect("localhost","root","123","mysite",charset='utf8')
    cursor = db.cursor()
    l,z,t=[],[],[]
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
                print sh.cell(0,col).value
            else:
                if col ==0:
                   __s_date = datetime.date(1899, 12, 31).toordinal()-1
                   d=datetime.date.fromordinal(__s_date+int(sh.cell(row,col).value))
                   value=d.strftime('%Y-%m-%d')
                   if value != date_test:
                       print "error:value equal date_test!"
                       break
                   t1.append(value)
                else:
                   t1.append(sh.cell(row,col).value)
        if row>0:
            z.append(zip(t,t1))
    s=z
    try:
        for i in range(0,len(s)):
            r=cursor.execute('select * from opt_optimization where date(date) = "%s"'%value)
            print r
            count=cursor.execute('select * from opt_optimization limit 0,%d'%r)
            t=cursor.fetchall()
            print "*****:%s"%count
            flag1=0
            if len(s[i])==10:
                print "*****",s[i][4][1],s[i][5][1],s[i][6][1],s[i][7][1],s[i][8][1]
                if s[i][4][1] ==0 or s[i][4][1]=="":
                    valide_cost=click_cost=appointment_cost=visit_cost=0
                else:
                    if isinstance(s[i][5][1],float) and int(s[i][5][1])>0:
                        click_cost=round(s[i][4][1]/s[i][5][1],2)
                    else:
                        print "xxxx",type(s[i][5][1])
                        click_cost=s[i][4][1]
                    if isinstance(s[i][6][1],float) and int(s[i][6][1])>0:
                        valide_cost=round(s[i][4][1]/s[i][6][1],2)
                    else:
                        valide_cost=s[i][4][1]
                    if isinstance(s[i][7][1],float) and int(s[i][7][1])>0:
                        appointment_cost=round(s[i][4][1]/s[i][7][1],2)
                    else:
                        appointment_cost=s[i][4][1]
                    if isinstance(s[i][8][1],float) and int(s[i][8][1])>0:
                        visit_cost=round(s[i][4][1]/s[i][8][1],2)
                    else:
                        visit_cost=s[i][4][1]
                sql="insert into opt_optimization values (null,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');\
                            "%(s[i][0][1],s[i][1][1],s[i][2][1],s[i][3][1],s[i][4][1],s[i][5][1],click_cost,s[i][6][1],s[i][7][1],s[i][8][1],valide_cost,\
                            appointment_cost,visit_cost,s[i][9][1])

            print sql
            if count >0:
                for j in  t:
                    if j[2] == s[i][1][1] and j[3] == s[i][2][1]  and j[4] == s[i][3][1] :
                        print "j[1]:%s s[i][0][1]:%s"%(j[1],s[i][0][1])
                        flag1=1

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
    f=[]
    for filename in glob.glob("/home/btc/data/changjiang/youhua_*"):
        f.append(filename)
        if os.path.isfile('%s'%filename) :
           print "yyyy"
           excel2mysql('%s'%filename)
if __name__ == "__main__":
    while(1):
        updateMysql()
        time.sleep(10)
