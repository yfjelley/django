#-*- coding:utf-8 -*-
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db import connection,transaction
from opt.models import Optimization
def opt_data(request):
    a=Optimization.objects.all()
    p=[['媒体','网站','地区','点击次数','有效量','预约量','就诊量','未就诊量']]
    for i in a:
        l=zip(['media','site','addres','click','valide','appointment','visit',\
                'unvisit'],[i.media,i.site,i.addres,i.click,i.valide,i.appointment,i.visit,i.unvisit])
        p.append(l)
    s=json.dumps(p)
    return render_to_response('test1.html',{'getsiteinfo':s})



def index(request):
    return HttpResponse("Hello,world.You're at the poll index.")
# Create your views here.
