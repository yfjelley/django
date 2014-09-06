#-*- coding:utf-8 -*-
import logging
import json
from datetime import datetime
from datetime import date
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db import connection,transaction
from django.template import RequestContext
from django.template import loader
from opt.models import Optimization
#from django.template import RequestContext
from templates import mysql
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
logger=logging.getLogger("django")

class DateEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,datetime):
            return obj.__str__()
        elif isinstance(obj,date):
            return obj.__str__()
        return json.JSONEncoder.default(self,obj)
def selection(request):
    a=Optimization.objects.values('media')
    p=[]
    for i in a:
        if i not in p:
            p.append(i)
    return HttpResponse(p)    

def getWeek():
    current = datetime.now()
    weekList = []
    yearList = []
    for i in range(1,13):
        for j in range(1,32):
            try:
                d = date(current.year,i,j)
                if len(weekList) == 0:
                    weekList.append(d)
                else:
                    if d.weekday()>weekList[-1].weekday():
                        weekList.append(d)
                    else:
                        yearList.append(weekList)
                        weekList = []
                        weekList.append(d)
            except Exception ,e:
     #            print e
                 pass
    return yearList
def whichWeek(d):
    w = getWeek()
    for i in range(len(w)):
        for j in w[i]:
            if d == j:
                return i+1

def dayReport(request):
    params = request.POST.copy()
    condition = {}
    logger.info("params:%s"%params)
    for k,v in params.iteritems():
        v = v.strip()
        if v != 'all':
            condition[k] = v
    a = Optimization.objects.filter(**condition)
    logger.info("a:%s"%a)    
    p=[]
    for i in a:
        l = [i.date,i.department,i.media,i.site,i.addres,i.cusume,i.click,round(i.cusume/i.click,2),\
                i.valide,i.appointment,i.visit,round(i.cusume/i.valide,2),round(i.cusume/i.appointment,2),\
                round(i.cusume/i.visit,2),i.unvisit]
        p.append(l)
        logger.info("i.date:%s"%i.date)
    if request.method == "GET":
        return render_to_response('day.html',{'tableInfo':p},context_instance = RequestContext(request))
    elif request.method == "POST":
        return render_to_response('table.html',{'tableInfo':p},context_instance = RequestContext(request))

def weekReport(request):
    date = None
    a = []
    nWeek = []
    week = getWeek()
    for i in range(1,len(week)+1):
        if i < 10:
           nWeek.append(str(datetime.now().year)+str(0)+str(i))
        else:
           nWeek.append(str(datetime.now().year)+str(i))

    params = request.POST.copy()
    if params.has_key("date") and params["date"] != "all":
        date = params.pop("date")
    condition = {}
    p=[]
    for k,v in params.iteritems():
        v = v.strip()
        if v != 'all':
            condition[k] = v
    if date:
        for i in week[int(date[0][-2:])-1]:        
            condition["date"] = i
            a = Optimization.objects.filter(**condition)
            for i in a:
                l = [whichWeek(i.date),i.department,i.media,i.site,i.addres,i.cusume,i.click,round(i.cusume/i.click,2),\
                        i.valide,i.appointment,i.visit,round(i.cusume/i.valide,2),round(i.cusume/i.appointment,2),\
                        round(i.cusume/i.visit,2),i.unvisit]
                p.append(l)
    else:
        a = Optimization.objects.filter(**condition)
        for i in a:
            l = [whichWeek(i.date),i.department,i.media,i.site,i.addres,i.cusume,i.click,round(i.cusume/i.click,2),\
                    i.valide,i.appointment,i.visit,round(i.cusume/i.valide,2),round(i.cusume/i.appointment,2),\
                    round(i.cusume/i.visit,2),i.unvisit]
            p.append(l)

    if request.method == "GET":
        return render_to_response('week.html',{'nWeek':nWeek,'tableInfo':p},context_instance = RequestContext(request))
    elif request.method == "POST":
        return render_to_response("selectWeek.html",{'nWeek':nWeek,'tableInfo':p},context_instance = RequestContext(request))
