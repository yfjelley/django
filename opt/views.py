#-*- coding:utf-8 -*-
import logging
import json
from datetime import datetime
from datetime import date
from templates import tab
from templates import tab_week
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
        elif isinstance(obj,date):
            return obj.__str__()
        return json.JSONEncoder.default(self,obj)
def opt_data(request):
    timeOpt=request.POST.get('timeOpt',)
    logger=logging.getLogger("django")
    logger.info("timeOpt:%s"%timeOpt)
    sql='select * from opt_optimization where date(date)="%s"'%timeOpt
    a=Optimization.objects.raw(sql)
    
    #a=Optimization.objects.all()
    p=[]
    for i in a:
        l=zip(["date",'media','site','addres','cusume','click','click_cost','valide','appointment','visit',\
                'valide_cost','appointment_cost','visit_cost','unvisit'],[i.date,i.media,i.site,i.addres,\
                i.cusume,i.click,i.click_cost,i.valide,i.appointment,i.visit,i.valide_cost,i.appointment_cost,\
                i.visit_cost,i.unvisit])
        p.append(l)
    s=json.dumps(p,cls=DateEncoder)
    try:
        tab.Tab(s)
    except Exception ,e:
        print e
    return render_to_response('test1.html',{'getsiteinfo':s})

def opt(request):
    return render_to_response('show.html',)
def opt_week(request):
    s1=[]
    for weekOpt in range(0,4):
        sql='SELECT * FROM opt_optimization WHERE YEARWEEK(date_format(date,"%%%%Y-%%%%m-%%%%d"))= YEARWEEK(now())-%d'%weekOpt
        print sql
        a=Optimization.objects.raw(sql)
        p=[]
        for i in a:
            print i.cusume
            l=zip(["date",'media','site','addres','cusume','click','click_cost','valide','appointment','visit',\
                    'valide_cost','appointment_cost','visit_cost','unvisit'],[i.date,i.media,i.site,i.addres,\
                    i.cusume,i.click,i.click_cost,i.valide,i.appointment,i.visit,i.valide_cost,i.appointment_cost,\
                    i.visit_cost,i.unvisit])
            p.append(l)
        logger=logging.getLogger("django")
        s1.append(p)
    s=json.dumps(s1,cls=DateEncoder)
    try:
        tab_week.Tab(s)
        logger.info("s:%s"%s)
    except Exception ,e:
        print e
    return render_to_response('week.html',{'getsiteinfo':s})


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
