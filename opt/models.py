from datetime import date
from django.db import models
class Optimization(models.Model):
    date = models.DateField(auto_now=True)
    department = models.CharField(max_length=40)
    media = models.CharField(max_length=40)
    site = models.CharField(max_length=40)
    addres = models.CharField(max_length=40)
    cusume = models.FloatField()
    click = models.IntegerField()
    valide = models.IntegerField()
    appointment = models.IntegerField()
    visit = models.IntegerField()
    unvisit = models.IntegerField()
#    date=models.DateTimeField(auto_now=True,blank=True,null= False)
#    date=models.DateTimeField(auto_now_add = True)

#    def __unicode__(self):
#        return self.media
#        return [self.media,self.site,self.addres,self.cusume,self.click,self.valide,self.appointment,self.visit,self.unvisit]

# Create your models here.
class coverage(models.Model):
    keywords = models.CharField(max_length=40)
    feature = models.CharField(max_length=40)
    rank = models.CharField(max_length=40)
