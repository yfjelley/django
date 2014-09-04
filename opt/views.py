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

def weekReport(request):
    s1=[]
    s2=[]
    for weekOpt in range(0,4):
        s3=[]
        s4=[]
        s5=[]
        sql='SELECT * FROM opt_optimization WHERE YEARWEEK(date_format(date,"%%%%Y-%%%%m-%%%%d"))= YEARWEEK(now())-%d'%weekOpt
        a=Optimization.objects.raw(sql)
        p=[]
        w=[]
        for i in a:
            s3.append([i.date,i.media,i.site,i.addres,i.cusume,i.click,i.valide,i.appointment,i.visit,i.unvisit])
            s5.append(i.date)
        s5=list(set(s5))
        for i in range(0,len(s3)):
            cusume_week=s3[i][4]
            click_week=s3[i][5]
            valide_week=s3[i][6]
            appointment_week=s3[i][7]
            visit_week=s3[i][8]
            unvisit_week=s3[i][9]
            for j in range(0,len(s3)):
                if s3[i][1] == s3[j][1] and s3[i][2] == s3[j][2] and s3[i][3] == s3[j][3] and s3[i][0] != s3[j][0]:
                    cusume_week+=s3[j][4]
                    click_week+=s3[j][5]
                    valide_week+=s3[j][6]
                    appointment_week+=s3[j][7]
                    visit_week+=s3[j][8]
                    unvisit_week+=s3[j][9]
            if click_week==0:
                click_cost=cusume_week
            else:
                click_cost=round(cusume_week/click_week,2)
            if valide_week==0:
                valide_cost=cusume_week
            else:
                valide_cost=round(cusume_week/valide_week,2)
            if appointment_week==0:
                appointment_cost=cusume_week
            else:
                appointment_cost=round(cusume_week/appointment_week,2)
            if visit_week==0:
                visit_cost=cusume_week
            else:
                visit_cost=round(cusume_week/visit_week,2)
            if unvisit_week==0:
                unvisit_cost=cusume_week
            else:
                unvisit_cost=cusume_week/unvisit_week
            w=[s3[i][1],s3[i][2],s3[i][3],cusume_week,click_week,click_cost,valide_week,appointment_week,visit_week,\
                    valide_cost,appointment_cost,visit_cost,unvisit_week]
            w.append(s5)
            p.append(w)
    logger.info("w:%s"%w)
    return render_to_response('week.html',{'weekInfo':p},context_instance = RequestContext(request))

def opt_site(request):
    s1=[]
    s2=[]
    for weekOpt in range(0,4):
        s3=[]
        s4=[]
        s5=[]
        sql='SELECT * FROM opt_optimization WHERE YEARWEEK(date_format(date,"%%%%Y-%%%%m-%%%%d"))= YEARWEEK(now())-%d'%weekOpt
        a=Optimization.objects.raw(sql)
        p=[]
        w=[]
        for i in a:
            s3.append([i.date,i.media,i.site,i.addres,i.cusume,i.click,i.valide,i.appointment,i.visit,i.unvisit])
            s5.append(i.date)
        s5=list(set(s5))
        d={}
        for i in s3:
            if i[1] not in d:
                d[i[1]]=[]
            d[i[1]].append(i)
        for k in d.keys():
            cusume_week=0
            click_week=0
            valide_week=0
            appointment_week=0
            visit_week=0
            unvisit_week=0
            for i in d[k]:
                cusume_week+=i[4]
                click_week+=i[5]
                valide_week+=i[6]
                appointment_week+=i[7]
                visit_week+=i[8]
                unvisit_week+=i[9]
            if click_week==0:
                click_cost=cusume_week
            else:
                click_cost=round(cusume_week/click_week,2)
            if valide_week==0:
                valide_cost=cusume_week
            else:
                valide_cost=round(cusume_week/valide_week,2)
            if appointment_week==0:
                appointment_cost=cusume_week
            else:
                appointment_cost=round(cusume_week/appointment_week,2)
            if visit_week==0:
                visit_cost=cusume_week
            else:
                visit_cost=round(cusume_week/visit_week,2)
            if unvisit_week==0:
                unvisit_cost=cusume_week
            else:
                unvisit_cost=cusune_week/unvisit_week
            w=[k,cusume_week,click_week,click_cost,valide_week,appointment_week,visit_week,\
                    valide_cost,appointment_cost,visit_cost,unvisit_week]
            l=zip(['media','cusume','click','click_cost','valide','appointment','visit',\
                    'valide_cost','appointment_cost','visit_cost','unvisit'],w)
            if l not in p:
                p.append(l)
        jsonobj={'data':p,'date':s5}
        s1.append(jsonobj)
    s=json.dumps(s1,cls=DateEncoder)
#    logger.info("s:%s"%s)
    try:
        tab_site.Tab(s)
    except Exception ,e:
        print e
    return render_to_response('site.html',{'getsiteinfo':s})
def opt(request):
    return render_to_response('show.html',)
def dayReport(request):
    params = request.POST.copy()
    condition = {}
    for k,v in params.iteritems():
        v = v.strip()
        if v != 'all':
            condition[k] = v
    a = Optimization.objects.filter(**condition)
    
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
    nWeek = []
    week = getWeek()
    for i in range(1,len(week)+1):
        if i < 10:
           nWeek.append(str(datetime.now().year)+str(0)+str(i))
        else:
           nWeek.append(str(datetime.now().year)+str(i))

    params = request.POST.copy()
    condition = {}
    for k,v in params.iteritems():
        v = v.strip()
        if v != 'all' and v != 'noall' and str(datetime.now().year) not in v:
            condition[k] = v
        if str(datetime.now().year) in v:
            for i in week[int(v[-2:])-1]:
                condition[k] = i
    a = Optimization.objects.filter(**condition)
    return render_to_response('week.html',{'nWeek':nWeek},context_instance = RequestContext(request))
def index(request):
    return render_to_response('index.html',)
