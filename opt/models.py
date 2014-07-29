from datetime import date
from django.db import models
class Optimization(models.Model):
    date=models.DateField(auto_now=True)
    media=models.CharField(max_length=40)
    site=models.CharField(max_length=40)
    addres=models.CharField(max_length=40)
    cusume=models.FloatField()
    click=models.IntegerField()
    click_cost=models.FloatField()
    valide=models.IntegerField()
    appointment=models.IntegerField()
    visit=models.IntegerField()
    valide_cost=models.FloatField()
    appointment_cost=models.FloatField()
    visit_cost=models.FloatField()
    unvisit=models.IntegerField()
#    date=models.DateTimeField(auto_now=True,blank=True,null= False)
#    date=models.DateTimeField(auto_now_add = True)

#    def __unicode__(self):
#        return self.media
#        return [self.media,self.site,self.addres,self.cusume,self.click,self.valide,self.appointment,self.visit,self.unvisit]

# Create your models here.
