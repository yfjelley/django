
__doc__ = """The pyh.py module is the core of the PyH package. PyH lets you
generate HTML tags from within your python code.
See http://code.google.com/p/pyh/ for documentation.
"""
__author__ = "Emmanuel Turlay <turlay@cern.ch>"
__version__ = '$Revision: 43 $'
__date__ = '$Date$'

from sys import _getframe, stdout, modules, version
nOpen={}

nl = '/n'
doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">/n'
charset = '<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />/n'

tags = ['html', 'body', 'head', 'link', 'meta', 'div', 'p', 'form', 'legend', 
        'input', 'select', 'span', 'b', 'i', 'option', 'img', 'script',
        'table', 'tr', 'td', 'th', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'fieldset', 'a', 'title', 'body', 'head', 'title', 'script', 'br', 'table','font']

selfClose = ['input', 'img', 'link', 'br']

class Tag(list):
    tagname = ''
    
    def __init__(self, *arg, **kw):
        self.attributes = kw
        if self.tagname : 
            name = self.tagname
            self.isSeq = False
        else: 
            name = 'sequence'
            self.isSeq = True
        self.id = kw.get('id', name)
        #self.extend(arg)
        for a in arg: self.addObj(a)

    def __iadd__(self, obj):
        if isinstance(obj, Tag) and obj.isSeq:
            for o in obj: self.addObj(o)
        else: self.addObj(obj)
        return self
    
    def addObj(self, obj):
        if not isinstance(obj, Tag): obj = str(obj)
        id=self.setID(obj)
        setattr(self, id, obj)
        self.append(obj)

    def setID(self, obj):
        if isinstance(obj, Tag):
            id = obj.id
            n = len([t for t in self if isinstance(t, Tag) and t.id.startswith(id)])
        else:
            id = 'content'
            n = len([t for t in self if not isinstance(t, Tag)])
        if n: id = '%s_%03i' % (id, n)
        if isinstance(obj, Tag): obj.id = id
        return id

    def __add__(self, obj):
        if self.tagname: return Tag(self, obj)
        self.addObj(obj)
        return self

    def __lshift__(self, obj):
        self += obj
        return obj

    def render(self):
        result = ''
        if self.tagname:
            result = '<%s%s%s>' % (self.tagname, self.renderAtt(), self.selfClose()*' /')
        if not self.selfClose():
            for c in self:
                if isinstance(c, Tag):
                    result += c.render()
                else: result += c
            if self.tagname: 
                result += '</%s>' % self.tagname
        result += '/n'
        return result

    def renderAtt(self):
        result = ''
        for n, v in self.attributes.iteritems():
            if n != 'txt' and n != 'open':
                if n == 'cl': n = 'class'
                result += ' %s="%s"' % (n, v)
        return result

    def selfClose(self):
        return self.tagname in selfClose        
    
def TagFactory(name):
    class f(Tag):
        tagname = name
    f.__name__ = name
    return f

thisModule = modules[__name__]

for t in tags: setattr(thisModule, t, TagFactory(t)) 

def ValidW3C():
    out = a(img(src='http://www.w3.org/Icons/valid-xhtml10', alt='Valid XHTML 1.0 Strict'), href='http://validator.w3.org/check?uri=referer')
    return out

class PyH(Tag):
    tagname = 'html'
    
    def __init__(self, name='MyPyHPage'):
        self += head()
        self += body()
        self.attributes = dict(xmlns='http://www.w3.org/1999/xhtml', lang='en')
        self.head += title(name)

    def __iadd__(self, obj):
        if isinstance(obj, head) or isinstance(obj, body): self.addObj(obj)
        elif isinstance(obj, meta) or isinstance(obj, link): self.head += obj
        else:
            self.body += obj
            id=self.setID(obj)
            setattr(self, id, obj)
        return self

    def addJS(self, *arg):
        for f in arg: self.head += script(type='text/javascript', src=f)

    def addCSS(self, *arg):
        for f in arg: self.head += link(rel='stylesheet', type='text/css', href=f)
    
    def printOut(self,file=''):
        if file: f = open(file, 'w')
        else: f = stdout
        f.write(doctype)
        f.write(self.render())
        f.flush()
        if file: f.close()
    
class TagCounter:
    _count = {}
    _lastOpen = []
    for t in tags: _count[t] = 0
    def __init__(self, name):
        self._name = name
    def open(self, tag):
        if isLegal(tag): 
            self._count[tag] += 1
            self._lastOpen += [tag]
    def close(self, tag):
        if isLegal(tag) and self._lastOpen[-1] == tag: 
            self._count[tag] -= 1
            self._lastOpen.pop()
        else:
            print 'Cross tagging is wrong'
    def isAllowed(self, tag, open):
        if not open and self.isClosed(tag):
            print 'TRYING TO CLOSE NON-OPEN TAG: %s' % tag
            return False
        return True
    def isOpen(self, tag):
        if isLegal(tag): return self._count[tag]
    def isClosed(self, tag):
        if isLegal(tag): return not self._count[tag]

    
def isLegal(tag):
    if tag in tags: return True
    else:
        print 'ILLEGAL TAG: %s' % tag
        return False
#第二步，写和DB交互的代码，通常写报表都需要从数据库或其他数据元获取数据。我的比较简单，源代码如下

#coding=utf-8
import loadmylib
import dbunit_mysql
from pyh import *

class dbreport:
 def __init__(self,dbinfo='report',project='aliuid',suitid=None):
  self.db = dbunit_mysql.DBUnit(dbinfo,project) 
  self.suitid = suitid
  if self.suitid <= 0:
   print "suitid must not be none"
   return
 #
 def get_taskresult_records(self):
  try:
   suitresult = self.db.read("SELECT * FROM ex_suit e where suitid =%d"%self.suitid)
   taskid = suitresult[0]['taskid']
   taskresult = self.db.read("select * from task where taskid = %d"%int(taskid))
   return taskresult[0]
  except:
   print "getsuitreport error"


 def get_groupresult_records(self):
  try:
   groupresult = self.db.read("SELECT * FROM ex_group where suitid =%d"%self.suitid)
   return groupresult
  except:
   print "getgroupreport error"
     
 
 def get_failedcase_records(self):
  try:
   sqlstr = "SELECT e.*,f.testgroupname FROM ex_case e left join ex_group f on e.testgroupid = f.testgroupid where f.suitid=%d and e.status =1 order by testcaseid"%self.suitid
   groupresult = self.db.read(sqlstr)
   return groupresult
  except:
   print "getgroupreport error"
  
 def get_totalcase_records(self):
  try:
   sqlstr = "SELECT e.*,f.testgroupname FROM ex_case e left join ex_group f on e.testgroupid = f.testgroupid where f.suitid=%d order by testcaseid"%self.suitid
   groupresult = self.db.read(sqlstr)
   return groupresult
  except:
   print "getgroupreport error"

 def getcaseresult():
  mytab.attributes[''] = '';  
  pass


if __name__ == '__main__':
 dbrp = dbreport(suitid=12)
 result = dbrp.get_failedcase_records()
 result1 = dbrp.get_totalcase_records()
 print len(result)
 print result
 print result1
#第三步，自然是生成报表的代码了。源代码如下

#coding=utf-8
import loadmylib
import dbunit_mysql
from pyh import *
import dbreport
import commonfunc
import config

class report:
 def __init__(self,dbinfo='report',project='aliuid',suitid=None):
  self.page = PyH('%s test report'%project)
  self.page << '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
  self.dbinfo = dbinfo
  self.project = project
  self.drp = dbreport.dbreport(dbinfo,project,suitid)

 #设定表格的格式
 def tablecss(self,table = None,width='90%'):
  table.attributes['cellSpacing'] = 1;  
  table.attributes['cellPadding'] = 1;  
  table.attributes['border'] = 1;  
  table.attributes['borderColor'] = '#666666';  
  table.attributes['width'] = width;  
 #set colum title bgcolor 
 def tr_title_css(self,tr = None):
  tr.attributes['bgcolor'] = '#CCCC00';  

 #get summary info
 def gentask_html(self):
  #get taskresult from mysqldb
  taskresult = self.drp.get_taskresult_records()
  sum_div = div(b('.摘要'), id='myCSSid1')  
  self.page << sum_div 
  interfaces = taskresult['modules']
  num_interface = len(interfaces.split(','))
  totalcase = int(taskresult['totalcase'])
  failedcase = int(taskresult['failedcase'])
  successcase = totalcase - failedcase
  tab_task = self.page << table()
  self.tablecss(tab_task)
  title_tr_task = tab_task << tr()
  self.tr_title_css(title_tr_task)
  #add task column title
  title_tr_task << td('测试模块数')   
  title_tr_task << td('通过用例数')
  title_tr_task << td('失败用例数')
  title_tr_task << td('总共用例数')
   #add column value
  value_tr_task = tab_task << tr()
  value_tr_task << td('%d'%num_interface)
  value_tr_task << td('%d'%successcase)
  value_tr_task << td('%d'%failedcase)
  value_tr_task << td('%d'%totalcase)
  self.page.printOut('test.html')     
  self.page << br()

     
 def gengroupreport(self):
  testgroups = self.drp.get_groupresult_records() 
  sum_div = div(b('.模块测试报告'), id='mydiv2')  
  self.page << sum_div 
  tab_group = self.page << table()
  self.tablecss(tab_group)
  title_tr_group = tab_group << tr()
  self.tr_title_css(title_tr_group)
  #add task column title
  title_tr_group << td('模块名称')   
  title_tr_group << td('测试结果')
  title_tr_group << td('通过用例数')
  title_tr_group << td('失败用例数')
  title_tr_group << td('总共用例数')
  for i in range(len(testgroups)):
   testgroup = testgroups[i]
   groupname = testgroup['testgroupname']
   groupstatus = int(testgroup['status'])
   totalcase = int(testgroup['totalcase'])
   failedcase = int(testgroup['failedcase'])
   successcase = totalcase - failedcase
    #add column value
   value_tr_group = tab_group << tr()
   value_tr_group << td('%s'%groupname)
   if groupstatus == 0: 
    value_tr_group << td('Pass')
   else:
    value_tr_group << td('Failed')
   value_tr_group << td('%d'%successcase)
   value_tr_group << td('%d'%failedcase)
   value_tr_group << td('%d'%totalcase)
  self.page << br()
 
 def gen_failedcase_report(self):
  failedcases = self.drp.get_failedcase_records()
  sum_div = div(b('.失败用例列表'), id='mydiv2')  
  self.page << sum_div 
  tab_failed_case = self.page << table()
  self.tablecss(tab_failed_case)
  title_tr_failed_case = tab_failed_case << tr()
  self.tr_title_css(title_tr_failed_case)
  #add task column title
  title_tr_failed_case << td('用例编号')   
  title_tr_failed_case << td('模块名称')
  title_tr_failed_case << td('用例说明')
  title_tr_failed_case << td('用例等级')
  title_tr_failed_case << td('测试结果')
  for i in range(len(failedcases)):
   testcase = failedcases[i]
   casecode = testcase['testcasename']
   groupname = testcase['testgroupname']
   description = testcase['description']
   level = testcase['caselevel']
   status = int(testcase['status'])
    #add column value
   value_tr_failed_case = tab_failed_case << tr()
   value_tr_failed_case << td('%s'%casecode)
   value_tr_failed_case << td('%s'%groupname)
   value_tr_failed_case << td('%s'%description.encode('utf-8'))
   value_tr_failed_case << td('%s'%level)
   if status == 0: 
    value_tr_failed_case << td('Pass')
   else:
    value_tr_failed_case << td('Failed')
  self.page << br()

 def gen_totalcase_report(self):
    totalcases = self.drp.get_totalcase_records()
    sum_div = div(b('.所有用例列表'), id='mydiv4')  
    self.page << sum_div 
    tab_total_case = self.page << table()
    self.tablecss(tab_total_case)
    title_tr_total_case = tab_total_case << tr()
    self.tr_title_css(title_tr_total_case)
    #add task column title
    title_tr_total_case << td('用例编号')   
    title_tr_total_case << td('模块名称')
    title_tr_total_case << td('用例说明')
    title_tr_total_case << td('用例等级')
    title_tr_total_case << td('测试结果')
    for i in range(len(totalcases)):
       testcase = totalcases[i]
       casecode = testcase['testcasename']
       groupname = testcase['testgroupname']
       description = testcase['description']
       level = testcase['caselevel']
       status = int(testcase['status'])
    #add column value
    value_tr_total_case = tab_total_case << tr()
    value_tr_total_case << td('%s'%casecode)
    value_tr_total_case << td('%s'%groupname)
    value_tr_total_case << td('%s'%description.encode('utf-8'))
    value_tr_total_case << td('%s'%level)
    if status == 0: 
       value_tr_total_case << td('Pass')
    else:
       value_tr_total_case << td('Failed')
       self.page << br()
  

 def getdev_build_info(self,section='build_dev'):
    import os
    build_dev = section
    self.build_dev_info = config.SysConfig(self.project).getdbconnectinfo(build_dev)
    host = self.build_dev_info['host']
    user = self.build_dev_info['user']
    pwd = self.build_dev_info['password']
    source = self.build_dev_info['source']
    result = commonfunc.ssh_cmd(host,user,pwd,"svn info %s"%source)
    lresult = result.split("/r/n")
    url = lresult[2]
    reversion = lresult[5]
    last_author = lresult[8]
    last_date = lresult[10] 
    return lresult

 def genbuildreport(self):
    dev_info = self.getdev_build_info('build_dev')
    test_info = self.getdev_build_info('build_test')
  
    build_div = div(b('.版本信息'), id='mydiv5')  
    self.page << build_div 
    tab_build = self.page << table()

    self.tablecss(tab_build,'70%')
    title_tr_build = tab_build << tr()
    self.tr_title_css(title_tr_build)
    #add task column title
    title_td = title_tr_build << td('开发代码版本信息')  
    title_td.attributes['colspan'] = '1';  
   
    #add column value
    value_tr_build = tab_build << tr()
    td_dev = value_tr_build << td()
    #td_dev.attributes['font'] = 'size =1'
    td_dev = td_dev << font()
    td_dev.attributes['size'] = '2'
    pt = td_dev << p()
    pt << dev_info[2].strip()
    pt <<br()
    pt << dev_info[5].strip()
    pt <<br()
    pt <<dev_info[8].strip()
    pt <<br()
    pt <<dev_info[10].strip()
  
    title_tr_build = tab_build << tr()
    self.tr_title_css(title_tr_build)
    #add task column title
    title_td = title_tr_build << td('测试代码版本信息')
    title_td.attributes['colspan'] = '1';  
    #add column value
    value_tr_build = tab_build << tr()
    td_test = value_tr_build << td()
    td_test = td_test << font()
    td_test.attributes['size'] = '2'
    pt = td_test << p()
    pt << test_info[2].strip()
    pt <<br()
    pt << test_info[5].strip()
    pt <<br()
    pt << test_info[8].strip()
    pt <<br()
    pt << test_info[10].strip()
    pt <<br()
    self.page << br()

 def genreport(self,filename='test.html'):
    self.genbuildreport()
    self.gentask_html()
    self.gengroupreport()
    self.gen_totalcase_report()
    self.page.printOut('test.html')     
  
  

if __name__ == '__main__':
    file = 'first.html'
    rp = report(suitid=12)
    rp.genreport(file)
