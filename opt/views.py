#-*- coding:utf-8 -*-
import logging,time
import json,math,urllib,urllib2,re,threading
from pyquery import PyQuery as pq
from django.shortcuts import render,render_to_response
from forms import UserForm
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from datetime import date
from django.db.models import Sum
from django.db import connection,transaction
from django.template import loader
from opt.models import Optimization
from opt.models import coverage
from opt.models import feature
from opt.models import keywords
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

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
@login_required
def dayReport(request):
    '''明细(日)视图'''
    params = request.POST.copy()
    logger.info("params:%s"%params)
    date,condition = paramsHandle(params)
    obj = dayTableData(date,condition)
    p=Paginator(obj,10)
    if request.method == "GET":
        if request.GET.get('pn'):
            if int(request.GET.get('pn'))>0:
                num=int(request.GET.get('pn'))
            else:
                num=1
        else:
            num=1
        logger.info("num:%s"%num)
        return render_to_response('day.html',{'tableInfo':p.page(num).object_list,'page':p.num_pages,'num':num},context_instance = RequestContext(request))
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
        condition['date'] = date[0]
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
        condition['date'] = date[0]
    logger.info("condition:%s"%condition)
    a = Optimization.objects.filter(**condition)
    logger.info("a:%s"%a)
    for i in a:
        l = [i.date,i.department,i.media,i.site,i.addres,i.cusume,i.click,round(i.cusume/i.click,2),\
                i.valide,i.appointment,i.visit,round(i.cusume/i.valide,2),round(i.cusume/i.appointment,2),\
                round(i.cusume/i.visit,2),i.unvisit]
        p.append(l)
    return p

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
def tableData(date,condition,group_by,nWeek):
    '''获取表格数据'''
    week = getWeek()
    p = []
    if date:
        logger.info("group_buy:%s"%group_by)
        condition["date__range"] = (week[int(date[0][-2:])-1][0],week[int(date[0][-2:])-1][6]) 
        p = weekSearch(condition,group_by,date[0])
    else:
        for w in nWeek:
            d = week[int(w[-2:])-1]
            condition["date__range"] = (d[0],d[len(d)-1])
            p +=weekSearch(condition,group_by,w)
    return p
@login_required
def weekReport(request):
    '''明细(周)视图'''
    a = []
    nWeek = weekList()
    params = request.POST.copy()
    date,condition = paramsHandle(params)
    group_by = ['department','media','site','addres']
    p =tableData(date,condition,group_by,nWeek)
    if request.method == "GET":
        return render_to_response('week.html',{'nWeek':nWeek,'tableInfo':p},context_instance = RequestContext(request))
    elif request.method == "POST":
        return render_to_response("selectWeek.html",{'nWeek':nWeek,'tableInfo':p},context_instance = RequestContext(request))

def weekAccountReport(request):
    '''站点汇总(周)'''
    a = []
    p = []
    nWeek = weekList()
    params = request.POST.copy()
    date,condition = paramsHandle(params)
    group_by = ['department','media','site']
    p =tableData(date,condition,group_by,nWeek)
    if request.method == "GET":
        return render_to_response('weekAccount.html',{'nWeek':nWeek,'tableInfo':p},context_instance = RequestContext(request))
    elif request.method == "POST":
        return render_to_response("selectWeekAccount.html",{'nWeek':nWeek,'tableInfo':p},context_instance = RequestContext(request))
def weekSearch(c,group_by,w=None):
    '''以周为单位汇总数据'''
    o = []
    a = Optimization.objects.filter(**c).values(*group_by).annotate(total_cusume=Sum('cusume'),\
            total_click=Sum('click'),total_valide=Sum('valide'),total_appointment=Sum('appointment'),total_visit=Sum('visit'),\
            total_unvisit=Sum('unvisit')).order_by(*group_by)
    for i in a:
        l = [w] if w else []
        for g in group_by:
            l.append(i["%s"%g])
        s = [i['total_cusume'],i['total_click'],round(i['total_cusume']/i['total_click'],2),\
                i['total_valide'],i['total_appointment'],i['total_visit'],round(i['total_cusume']/i['total_valide'],2),\
                round(i['total_cusume']/i['total_appointment'],2),round(i['total_cusume']/i['total_visit'],2),i['total_unvisit']]
        l += s
        logger.info("l:%s"%l)
        o.append(l)
    return o

def index(request):
    #用户request.GET.get()面
    return render(request,'reg.html')

def register(request):
    #注册提交
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid() and form.clean_password():
            logger.info("form validation")
            new_user = User.objects.create_user(request.POST['userName'], request.POST['userEmail'], request.POST['userPassword'])
            new_user.save()
            return render_to_response('day.html')
        else:
            return render(request,'register.html', {'form':form})
    #超链接点击过来的注册
    else:
        return render(request,'register.html')
    
def login(request):
    #表单提交过来的数据
    if request.user.is_authenticated():
        #dayReport(request)
        return  render_to_response('day.html')
    if request.method == 'POST':
        userName = request.POST['userName']
        userPassword = request.POST['password']
        user = authenticate(username=userName, password=userPassword)
        if user is not None:
            if user.is_active:
               user_login(request, user)
               return render_to_response('day.html')
            else:
               return HttpResponse('用户没有启用!')
        else:
            return HttpResponse('用户名或者密码错误！')
    else:
        return render_to_response('login.html')
    
def logout(request):
    user_logout(request)
    return render_to_response('login.html')
def upload(request):
    return render_to_response('uploadfile.html')
def jump(request):
    content=[]
    ft=request.GET['feature'].split(';')
    #去掉空字符串(如果feature末尾有';',会有一个空的字符串)
    try:
        ft.remove('')
    except Exception,e:
        pass
    #关键词去重
    kw=list(set(request.GET['keywords'].split('\n')))
    try:
        kw.remove('')
    except Exception,e:
        print e
        pass
    for i in kw:
        for j in ft:
            qs=coverage.objects.filter(keywords="%s"%i).filter(feature="%s"%j)
            for o in qs:
                if [o.keywords,o.feature,o.cov,o.rank] not in content:
                   content.append([o.keywords,o.feature,o.cov,o.rank])
    return render_to_response('coverageRank.html',{'content':content})
def cov(request):
    return render_to_response('coverage.html')
def worker(kws,fts):
    content = []
    for kw in kws:
        time.sleep(1)
        try:
            d = pq("http://www.baidu.com/s?wd=%s"%kw)
            logger.info("kw:%s"%kw)
            #获取百度快照链接
            link = d('a[data-nolog]')
            for i in range(len(d('.result.c-container'))):
                try:
                    #提取搜索的页面标题，如果标题中没有特征码，则打开百度快照
                    x=d('.result.c-container:eq(%d)'%i).text()
                    logger.info("fts:%s"%fts)
                    for ft in fts:
                        m=re.search(ft,x.decode('utf8'))
                        if m:
                            logger.info("ft:%s"%ft)
                            if len(content) != 0:
                               for j in content:
                                   if j[:2] == [kw,ft]:
                                       j[2].append(i+1)
                                       logger.info("ftssss:%s"%fts)
                                   else:
                                       if j == content[-1]:
                                            content.append([kw,ft,[i+1]])
                                       logger.info("xxxxs:%s"%fts)
                            else:
                               content.append([kw,ft,[i+1]])
                            logger.info("del:%s"%i)
                            try:
                                del link[i]
                            except Exception,e:
                                print "del link error:%s"%e
                                pass
                            logger.info("xs:%s"%fts)
                except Exception,e:
                    print "search baidu kuaizhao error:%s"%e
                    pass
            for i in range(len(link)):
                time.sleep(1)
                try:
                    href = d(link[i]).attr('href')
                    print href
                    #打开百度快照页
                    req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Accept':'text/html;q=0.9,*/*;q=0.8',
                     'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                    'Accept-Encoding':'gzip',
                    'Connection':'close','Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
                     }
                    req_timeout = 5
                    req = urllib2.Request("%s"%href,None,req_header)
                    h = urllib2.urlopen(req,None,req_timeout).read()
                    #h=urllib.urlopen('%s'%href).read()
                    html = h.decode('gb18030').encode('utf8')
                    for ft in fts:
                        m = re.search(ft,str(html))
                        if m:
                            if len(content) != 0 :
                               for j in content:
                                   if j[:2] == [kw,ft]:
                                       j[2].append(i+1)
                                   else:
                                       content.append([kw,ft,[i+1]])
                            else:
                                if j == content[-1]:
                                   content.append([kw,ft,[i+1]])
                except Exception,e:
                    print "urllib error:%s"%e
                    pass
        except Exception,e:
            print "error:%s"%e
            pass
    map(lambda x:x.insert(2,len(list(set(x[2])))),content)
    for i in content:
        coverage.objects.filter(keywords=i[0]).filter(feature=i[1]).delete()
        p1=coverage(None,i[0],i[1],i[2],list(set(i[3])),None)
        p1.save()
    logger.info("content:%s"%content)
    return content
def commit(request):
    content=[]
    print request.method
    if request.method == "GET":
        return render_to_response('coverage_commit.html')
    if request.method == "POST":
        print request.POST
        ft=request.POST['feature'].split(';')
        print ft
        #去掉空字符串(如果feature末尾有';',会有一个空的字符串)
        try:
            ft.remove('')
        except Exception,e:
            pass
        try:
            for i in ft:
                feature.objects.filter(feature=i).delete()
                p1=feature(None,i,None)
                p1.save()
        except Exception,e:
            print e
            pass
        #关键词去重
        kw=list(set(request.POST['keywords'].split('\n')))
        try:
            kw.remove('')
        except Exception,e:
            print e
            pass
        try:
            for i in kw:
                if i != '':
                   keywords.objects.filter(keywords=i).delete()
                   p1 = keywords(None,i,None)
                   p1.save()
        except Exception,e:
            print e
            pass
        return render_to_response('commitsuccess.html')
def commitsuc(request):
    return render_to_response('commitsuccess.html')
