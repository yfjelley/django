#-*- coding:utf-8 -*-
from pyh import *
import json
def Tab(b):
    s=json.loads(b)
    page = PyH('长江医院')
    page.addCSS('/static/css/bootstrap.min.css')
    page.addCSS('/static/css/bootstrap-responsiv.css')
    page.addCSS('/static/css/dataTables.bootstra.css')
    page.addJS('/static/js/dataTables.bootstra.js')
    page.addJS('/static/js/jquery.js')
    page.addJS('/static/js/jquery.dataTables.js')
    page.addJS('/static/js/bootstrap.min.js')
    page.addJS('/static/js/table.js')
    page << h2('推广站分析表',align='center')
    mytab=page<<table()
    mytab.attributes['class'] = "table table-striped table-bordered table-hover datatable"; 
    mytab<<thead(tr(th("日期")+th('部门')+th('媒体') + th('网站')+ th('地区')+ th('消费')+th('点击次数')+ th('点击成本')+th('有效量')+ th('预约量')+ th('就诊量')+ \
            th('有效成本')+th('预约成本')+th('就诊成本')+th('未就诊量')))
    if s:
        mybody=mytab<<tbody()
        for i in range(0,len(s)):
            mytr=mybody<<tr()
            for j in range(0,len(s[i])):
                mytr<<td('%s' %s[i][j][1])
    page.printOut("/usr/local/lib/python2.7/dist-packages/django/bin/myste/opt/templates/test1.html")
if __name__  == "__main__":
    Tab(s)

