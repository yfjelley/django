#-*- coding:utf-8 -*-
from pyh import *
import json
s='[[["media", "xinlang"], ["site", "www.xinlang.com"], ["addres", "hubei"], ["click", 9], ["valide", 5], ["appointment", 3], ["visit", 5], ["unvisit", 1]], [["media", "baidu"], ["site", "www.baidu.com"], ["addres", "shanghai"], ["click", 1000], ["valide", 5], ["appointment", 2], ["visit", 2], ["unvisit", 0]]]' 
def Tab(b):
    s=json.loads(b)
    page = PyH('长江医院')
    page.addCSS('/static/common.css')
    page << h2('推广站分析表',align='center')
    mytab=page<<table(caption="推广站分析表",align='center')
    mytab.attributes['cellSpacing'] = 0;  
    mytab.attributes['cellPadding'] = 0;  
    mytab.attributes['border'] = 1;  
    mytab.attributes['borderColor'] = '#666666';  
    mytab.attributes['width'] = 1050; 
    mytab<<tr(th("日期")+th('媒体') + th('网站')+ th('地区')+ th('点击次数')+ th('有效量')+ th('预约量')+ th('就诊量')+ th('未就诊量'))
    if s:
        for i in range(0,len(s)):
            mytr=mytab<<tr()
            for j in range(0,len(s[i])):
                mytr<<td('%s' %s[i][j][1])
    page.printOut("/usr/local/lib/python2.7/dist-packages/django/bin/myste/opt/templates/test1.html")
if __name__  == "__main__":
    Tab(s)

