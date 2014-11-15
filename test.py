from django.conf import settings
settings.configure()
import logging,time
logging.basicConfig()
from opt.models import keywords
a=keywords.objects.all()
for i in a:
    print i.keywords
