#-*- coding:utf-8 -*-
import logging
import json
from datetime import datetime
from datetime import date
from templates import tab
from templates import tab_week
from templates import tab_site
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
def opt_data(request):
    params = request.POST.copy()
    condition = {}
    logger.info("condition:%s"%condition)
    logger.info("params:%s"%params)
    for k,v in params.iteritems():
        v = v.strip()
        if v != 'all':
            condition[k] = v
            logger.info("condition:%s"%condition)
    a = Optimization.objects.filter(**condition)
    
    p=[]
    for i in a:
        l=zip(["date",'department','media','site','addres','cusume','click','click_cost','valide','appointment','visit',\
                'valide_cost','appointment_cost','visit_cost','unvisit'],[i.date,i.department,i.media,i.site,i.addres,\
                i.cusume,i.click,round(i.cusume/i.click,2),i.valide,i.appointment,i.visit,round(i.cusume/i.valide,2),round(i.cusume/i.appointment,2),\
                round(i.cusume/i.visit,2),i.unvisit])
        p.append(l)
        logger.info("p:%s"%p)
    s=json.dumps(p,cls=DateEncoder)
    try:
        tab.Tab(s)
    except Exception ,e:
        print e
    return render_to_response('test1.html',{'getsiteinfo':s})

def opt(request):
    media=Optimization.objects.values('media')
    media_option=[]
    for i in media:
        if i['media'] not in media_option:
            media_option.append(i['media'])
    #media_option=json.dumps(media_option)

    site=Optimization.objects.values('site')
    site_option=[]
    for i in site:
        if i['site'] not in site_option:
            site_option.append(i['site'])
    #site_option=json.dumps(site_option)
    
    department = Optimization.objects.values('department')
    dep_option=[]
    for i in department:
        if i['department'] not in dep_option:
            dep_option.append(i['department'])
    #dep_option=json.dumps(dep_option)

    addres = Optimization.objects.values('addres')
    addres_option = []
    for i in addres:
        if i['addres'] not in addres_option:
            addres_option.append(i['addres'])
    #addres_option=json.dumps(addres_option)
    return render_to_response('show.html',{'media':media_option,'site':site_option,'department':dep_option,'addres':addres_option})
def opt_week(request):
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
            l=zip(['media','site','addres','cusume','click','click_cost','valide','appointment','visit',\
                    'valide_cost','appointment_cost','visit_cost','unvisit'],w)
            if l not in p:
                p.append(l)
        jsonobj={'data':p,'date':s5}
        s1.append(jsonobj)
    s=json.dumps(s1,cls=DateEncoder)
    logger.info("s:%s"%s)
    try:
        tab_week.Tab(s)
    except Exception ,e:
        print e
    return render_to_response('week.html',{'getsiteinfo':s})

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
                unvisit_cost=cusume_week/unvisit_week
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
def dayReport(request):
    return render_to_response('day.html',)
def weekReport(request):
    return render_to_response('week.html',)
def monthReport(request):
    return render_to_response('month.html',)
def index(request):
    return render_to_response('index.html',)
