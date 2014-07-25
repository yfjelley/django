#-*- coding:utf-8 -*-
import logging
import json
from datetime import datetime
from templates import tab
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db import connection,transaction
from opt.models import Optimization
from templates import mysql
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
class DateEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,datetime):
            return obj.__str__()
        return json.JSONEncoder.default(self,obj)
def opt_data(request):
    mysql.updateMysql()
    a=Optimization.objects.all()
    p=[]
    for i in a:
        l=zip(["date",'media','site','addres','click','valide','appointment','visit',\
                'unvisit'],[i.date,i.media,i.site,i.addres,i.click,i.valide,i.appointment,i.visit,i.unvisit])
        p.append(l)
    s=json.dumps(p,cls=DateEncoder)
    logger=logging.getLogger("django")
    logger.debug("debugvvvvvvv")
    logger.info("aaaaaaaaaaa")
    try:
        tab.Tab(s)
    except Exception ,e:
        print e
    return render_to_response('test1.html',{'getsiteinfo':s})

def opt(request):
    return render_to_response('show.html',)
