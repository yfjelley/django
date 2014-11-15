# -*- coding:utf-8 -*-
from django.conf import settings
settings.configure()
if not settings.configured:
   settings.configure(DATABASES=settings.DATABASES)
import urllib2
from datetime import datetime
import time,os,logging,sys
logging.basicConfig()
from opt.models import keywords
from opt.models import coverage
from opt.models import feature
from django.db import models
reload(sys).setdefaultencoding('utf8')
LEVEL = logging.ERROR
logging.getLogger('apscheduler.executors.default').setLevel(LEVEL)
def worker():
    #os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
    print(keywords.objects.all())
    return
    kws,fts = [],[]
    for m in keywords.objects.all():
        if m not in kws:
           kws.append(m.keywords)
    for m in feature.objects.all():
        if m not in fts:
           fts.append(m.feature)
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
if __name__ == '__main__':
    worker()
