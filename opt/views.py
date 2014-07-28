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
#from django.template import RequestContext
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
    timeOpt=request.POST.get('timeOpt',)
    logger=logging.getLogger("django")
    logger.info("timeOpt:%s"%timeOpt)
    sql='select * from opt_optimization where date=%s'%timeOpt
    a=Optimization.objects.raw(sql)
    
    #a=Optimization.objects.all()
    p=[]
    for i in a:
        l=zip(["date",'media','site','addres','click','valide','appointment','visit',\
                'unvisit'],[i.date,i.media,i.site,i.addres,i.click,i.valide,i.appointment,i.visit,i.unvisit])
        p.append(l)
    s=json.dumps(p,cls=DateEncoder)
    try:
        tab.Tab(s)
    except Exception ,e:
        print e
    return render_to_response('test1.html',{'getsiteinfo':s})

def opt(request):
    return render_to_response('show.html',)

def opt_day(request):
    sql='select * from opt_optimization where TO_DAYS(NOW()) -TO_DAYS(date)<0'
    a=Optimization.objects.raw(sql)
    p=[]
    for i in a:
        l=zip(["date",'media','site','addres','click','valide','appointment','visit',\
                'unvisit'],[i.date,i.media,i.site,i.addres,i.click,i.valide,i.appointment,i.visit,i.unvisit])
        p.append(l)
    s=json.dumps(p,cls=DateEncoder)
    logger=logging.getLogger("django")
    try:
        tab.Tab(s)
    except Exception ,e:
        print e
    return render_to_response('test1.html',{'getsiteinfo':s})

def op(request):
    return render_to_response('show.html',)
