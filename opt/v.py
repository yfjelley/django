#-*- coding:utf-8 -*-
import json
#import templates.tab
from templates import tab
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db import connection,transaction
from opt.models import Optimization
def opt_data(request):
    a=Optimization.objects.all()
    p=[]
    for i in a:
        l=zip(['media','site','addres','click','valide','appointment','visit',\
                'unvisit'],[i.media,i.site,i.addres,i.click,i.valide,i.appointment,i.visit,i.unvisit])
        p.append(l)
    s=json.dumps(p)
    try:
        tab.Tab(s)
    except Exception ,e:
        print e
    return render_to_response('test1.html',{'getsiteinfo':s})
s=opt_data()
