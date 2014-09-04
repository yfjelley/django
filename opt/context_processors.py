from opt.models import Optimization
import logging
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
logger = logging.getLogger("django")

def custom_proc(request):
    media=Optimization.objects.values('media')
    media_option=[]
    for i in media:
        if i['media'] not in media_option:
            media_option.append(i['media'])

    site=Optimization.objects.values('site')
    site_option=[]
    for i in site:
        if i['site'] not in site_option:
            site_option.append(i['site'])
    
    department = Optimization.objects.values('department')
    dep_option=[]
    for i in department:
        if i['department'] not in dep_option:
            dep_option.append(i['department'])
    logger.info("department_option:%s"%dep_option)

    addres = Optimization.objects.values('addres')
    addres_option = []
    for i in addres:
        if i['addres'] not in addres_option:
            addres_option.append(i['addres'])

    return {'media':media_option,'site':site_option,'department':dep_option,'addres':addres_option}
    
