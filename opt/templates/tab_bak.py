# -*- coding:utf-8 -*-
from pyh import *
import json
b='[[["media", "xinlang"], ["site", "www.xinlang.com"], ["addres", "hubei"], ["click", 9], ["valide", 5], ["appointment", 3], ["visit", 5], ["unvisit", 1]], [["media", "baidu"], ["site", "www.baidu.com"], ["addres", "shanghai"], ["click", 1000], ["valide", 5], ["appointment", 2], ["visit", 2], ["unvisit", 0]]]' 
s=json.loads(b)
page = PyH('推广站分析表')
page << h2('推广站分析表')
mytab=page<<table()
mytab.attributes['cellSpacing'] = 0;  
mytab.attributes['cellPadding'] = 0;  
mytab.attributes['border'] = 1;  
mytab.attributes['borderColor'] = '#666666';  
mytab.attributes['width'] = 800;  
mytab<<tr(td('媒体') + td('网站')+ td('地区')+ td('点击次数')+ td('有效量')+ td('预约量')+ td('就诊量')+ td('未就诊量'))
if s:
    for i in range(0,len(s)):
#        mytr=mytab<<table width="200" border="1" cellspacing="0" cellpadding="0">
        mytr=mytab<<tr()
        for j in range(0,len(s[i])):
            mytr<<td('%s' %s[i][j][1])
page.printOut("test1.html")
