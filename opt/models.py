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
class coverage(models.Model):
    keywords = models.CharField(max_length=40)
    feature = models.CharField(max_length=40)
    cov = models.IntegerField()
    rank = models.CharField(max_length=40)
    date =  models.DateTimeField(auto_now=True)
class keywords(models.Model):
    keywords = models.CharField(max_length=40)
    date =  models.DateTimeField(auto_now=True)
class feature(models.Model):
    feature = models.CharField(max_length=40)
    date =  models.DateTimeField(auto_now=True)
