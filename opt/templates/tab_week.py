#-*- coding:utf-8 -*-
from pyh import *
import json
import logging
def Tab(b):
    logger=logging.getLogger("django")
    if len(b)>0:
        s=json.loads(b)
        logger=logging.getLogger("django")
        logger.info("tab_s%s"%s)
        logger.info("%s"%len(s))
        page = PyH('长江医院')
        page.addCSS('/static/common.css')
        for week in  range(0,len(s)):
            if len(s[week])==0:
                continue
            else:
                page << h2('推广站分析表周汇总',align='center')
                mytab=page<<table(caption="推广站分析表",align='center')
                mytab.attributes['cellSpacing'] = 0;  
                mytab.attributes['cellPadding'] = 0;  
                mytab.attributes['border'] = 1;  
                mytab.attributes['borderColor'] = '#666666';  
                mytab.attributes['width'] = 1300; 
                mytab<<tr(th("日期")+th('媒体') + th('网站')+ th('地区')+ th('消费')+th('点击次数')+ th('点击成本')+th('有效量')+ th('预约量')+ th('就诊量')+ \
                        th('有效成本')+th('预约成本')+th('就诊成本')+th('未就诊量'))
                if s[week]:
                    logger.info("%s"%s)
                    for i in range(0,len(s[week])):
                        mytr=mytab<<tr()
                        logger.info("%s"%s[week][i])
                        for j in range(0,len(s[week][i])):
                            mytr<<td('%s' %s[week][i][j][1])
    page.printOut("/usr/local/lib/python2.7/dist-packages/django/bin/myste/opt/templates/week.html")
if __name__  == "__main__":
    Tab(b)

