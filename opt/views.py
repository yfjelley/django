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
            for j in range(i,len(s3)):
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
    logger=logging.getLogger("django")
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
        for i in range(0,len(s3)):
            cusume_week=s3[i][4]
            click_week=s3[i][5]
            valide_week=s3[i][6]
            appointment_week=s3[i][7]
            visit_week=s3[i][8]
            unvisit_week=s3[i][9]
            for j in range(0,len(s3)):
                if s3[i][1] == s3[j][1] :

                    logger=logging.getLogger("django")
                    logger.info("s:%s"%s3[j][4])
                    cusume_week+=s3[j][4]
                    click_week+=s3[j][5]
                    valide_week+=s3[j][6]
                    appointment_week+=s3[j][7]
                    visit_week+=s3[j][8]
                    unvisit_week+=s3[j][9]
                logger.info("s:%s"%cusume_week)
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
            w=[s3[i][1],cusume_week,click_week,click_cost,valide_week,appointment_week,visit_week,\
                    valide_cost,appointment_cost,visit_cost,unvisit_week]
            l=zip(['media','cusume','click','click_cost','valide','appointment','visit',\
                    'valide_cost','appointment_cost','visit_cost','unvisit'],w)
            if l not in p:
                p.append(l)
        jsonobj={'data':p,'date':s5}
        s1.append(jsonobj)
    s=json.dumps(s1,cls=DateEncoder)
    logger=logging.getLogger("django")
#    logger.info("s:%s"%s)
    try:
        tab_site.Tab(s)
    except Exception ,e:
        print e
    return render_to_response('site.html',{'getsiteinfo':s})

"""def opt_day(request):
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
    return render_to_response('show.html',)"""
