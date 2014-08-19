#-*- coding:utf-8 -*-
from pyh import *
import json
import logging
import calendar
def Tab(b):
    logger=logging.getLogger("django")
    if len(b)>0:
        s=json.loads(b)
        page = PyH('长江医院')
        page.addCSS('/static/common.css')
        for week in  range(0,len(s)):
            if len(s[week]['data'])==0:
                logger.info("tab_week_len:%s"%len(s[week]['date']))
                continue
            else:
                logger.info("tab_week:%s"%len(s))
                page << h2('推广站分析表周汇总',align='center')
                page << h2('%s'%[i.encode("utf8") for i in s[week]['date']],align='center')
#                page << h2({%for i in s[week]['date']%} {{i}} {%endfor%},align='center')
                mytab=page<<table(caption="推广站分析表",align='center')
                mytab.attributes['cellSpacing'] = 0;  
                mytab.attributes['cellPadding'] = 0;  
                mytab.attributes['border'] = 1;  
                mytab.attributes['borderColor'] = '#666666';  
                mytab.attributes['width'] = 1300; 
                mytab<<tr(th('媒体') + th('网站')+ th('地区')+ th('消费')+th('点击次数')+ th('点击成本')+th('有效量')+ th('预约量')+ th('就诊量')+ \
                        th('有效成本')+th('预约成本')+th('就诊成本')+th('未就诊量'))
                if s[week]['data']:
                    for i in range(0,len(s[week]['data'])):
                        mytr=mytab<<tr()
                        for j in range(0,len(s[week]['data'][i])):
                            mytr<<td('%s' %s[week]['data'][i][j][1])
    page.printOut("/usr/local/lib/python2.7/dist-packages/django/bin/myste/opt/templates/week_bak.html")
if __name__  == "__main__":
    Tab(b)

