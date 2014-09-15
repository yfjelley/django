#-*- coding:utf-8 -*-
import logging
import json
from datetime import datetime
from datetime import date
from django.db.models import Sum
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

def getWeek():
    '''获取周和日期列表 '''
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
    '''计算日期是一年中的第几周'''
    w = getWeek()
    for i in range(len(w)):
        for j in w[i]:
            if d == j:
                return i+1

def dayReport(request):
    '''明细(日)视图'''
    params = request.POST.copy()
    date,condition = paramsHandle(params)
    p = dayTableData(date,condition)
    if request.method == "GET":
        return render_to_response('day.html',{'tableInfo':p},context_instance = RequestContext(request))
    elif request.method == "POST":
        return render_to_response('table.html',{'tableInfo':p},context_instance = RequestContext(request))
def dayAccountReport(request):
    '''明细(日)视图'''
    params = request.POST.copy()
    date,condition = paramsHandle(params)
    p = dayAccountTableData(date,condition)
    if request.method == "GET":
        return render_to_response('dayAccount.html',{'tableInfo':p},context_instance = RequestContext(request))
    elif request.method == "POST":
        return render_to_response('tableAccount.html',{'tableInfo':p},context_instance = RequestContext(request))
def dayAccountTableData(date,condition):
    p=[]
    if date:
        condition['date'] = date
    a = Optimization.objects.filter(**condition).values('date','department','media','site').annotate(total_cusume=Sum('cusume'),\
            total_click=Sum('click'),total_valide=Sum('valide'),total_appointment=Sum('appointment'),total_visit=Sum('visit'),\
                        total_unvisit=Sum('unvisit')).order_by('date','department','media','site')
    for i in a:
        l = [i['date'],i['department'],i['media'],i['site'],i['total_cusume'],i['total_click'],round(i['total_cusume']/i['total_click'],2),\
                i['total_valide'],i['total_appointment'],i['total_visit'],round(i['total_cusume']/i['total_valide'],2),round(i['total_cusume']/i['total_appointment'],2),\
                round(i['total_cusume']/i['total_visit'],2),i['total_unvisit']]
        p.append(l)
    return p

def dayTableData(date,condition):
    p=[]
    if date:
        condition['date'] = date
    a = Optimization.objects.filter(**condition)
    logger.info("a:%s"%a)
    for i in a:
        l = [i.date,i.department,i.media,i.site,i.addres,i.cusume,i.click,round(i.cusume/i.click,2),\
                i.valide,i.appointment,i.visit,round(i.cusume/i.valide,2),round(i.cusume/i.appointment,2),\
                round(i.cusume/i.visit,2),i.unvisit]
        p.append(l)
    return p

def weekList():
    '''生成周日历(201401...)'''
    nWeek = []
    week = getWeek()
    for i in range(1,len(week)+1):
        if i < 10:
           nWeek.append(str(datetime.now().year)+str(0)+str(i))
        else:
           nWeek.append(str(datetime.now().year)+str(i))
    return nWeek
def paramsHandle(params):
    '''周报表中的参数处理'''
    date = None
    condition = {}
    if params.has_key("date") and params["date"] != "all":
        date = params.pop("date")
    for k,v in params.iteritems():
        v = v.strip()
        if v != 'all':
            condition[k] = v
    return date,condition
def tableData(date,week,condition,group_by,nWeek):
    '''获取表格数据'''
    p = []
    if date:
        condition["date__range"] = (week[int(date[0][-2:])-1][0],week[int(date[0][-2:])-1][6]) 
        p = weekSearch(condition,date[0],group_by)
    else:
        for w in nWeek:
            d = week[int(w[-2:])-1]
            condition["date__range"] = (d[0],d[len(d)-1])
            p = weekSearch(condition,w,group_by)
    return p
def weekReport(request):
    '''明细(周)视图'''
    a = []
    nWeek = weekList()
    week = getWeek()
    params = request.POST.copy()
    date,condition = paramsHandle(params)
    group_by = ['department','media','site','addres']
    p =tableData(date,week,condition,group_by,nWeek)
    if request.method == "GET":
        return render_to_response('week.html',{'nWeek':nWeek,'tableInfo':p},context_instance = RequestContext(request))
    elif request.method == "POST":
        return render_to_response("selectWeek.html",{'nWeek':nWeek,'tableInfo':p},context_instance = RequestContext(request))

def weekAccountReport(request):
    '''站点汇总(周)'''
    a = []
    p = []
    nWeek = weekList()
    week = getWeek()
    params = request.POST.copy()
    date,condition = paramsHandle(params)
    group_by = ['department','media','site']
    p =tableData(date,week,condition,group_by,nWeek)
    if request.method == "GET":
        return render_to_response('weekAccount.html',{'nWeek':nWeek,'tableInfo':p},context_instance = RequestContext(request))
    elif request.method == "POST":
        return render_to_response("selectWeekAccount.html",{'nWeek':nWeek,'tableInfo':p},context_instance = RequestContext(request))
def weekSearch(c,w,group_by):
    '''以周为单位汇总数据'''
    o = []
    a = Optimization.objects.filter(**c).values(*group_by).annotate(total_cusume=Sum('cusume'),\
            total_click=Sum('click'),total_valide=Sum('valide'),total_appointment=Sum('appointment'),total_visit=Sum('visit'),\
            total_unvisit=Sum('unvisit')).order_by(*group_by)
    for i in a:
        l = [w]
        for g in group_by:
            l.append(i["%s"%g])
        s = [i['total_cusume'],i['total_click'],round(i['total_cusume']/i['total_click'],2),\
                i['total_valide'],i['total_appointment'],i['total_visit'],round(i['total_cusume']/i['total_valide'],2),\
                round(i['total_cusume']/i['total_appointment'],2),round(i['total_cusume']/i['total_visit'],2),i['total_unvisit']]
        l += s
        o.append(l)
    return o
def daySearch(c,group_by):
    '''以周为单位汇总数据'''
    o = []
    a = Optimization.objects.filter(**c).values(*group_by).annotate(total_cusume=Sum('cusume'),\
            total_click=Sum('click'),total_valide=Sum('valide'),total_appointment=Sum('appointment'),total_visit=Sum('visit'),\
            total_unvisit=Sum('unvisit')).order_by(*group_by)
    for i in a:
        l = []
        for g in group_by:
            l.append(i["%s"%g])
        s = [i['total_cusume'],i['total_click'],round(i['total_cusume']/i['total_click'],2),\
                i['total_valide'],i['total_appointment'],i['total_visit'],round(i['total_cusume']/i['total_valide'],2),\
                round(i['total_cusume']/i['total_appointment'],2),round(i['total_cusume']/i['total_visit'],2),i['total_unvisit']]
        l += s
        o.append(l)
    return o
