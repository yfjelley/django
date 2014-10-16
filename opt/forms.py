# -*- coding:utf-8 -*-
from django import forms
import sys
reload(sys)
sys.setdefaultencoding("utf8")
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    password = forms.CharField(label='再次输入密码',widget=forms.PasswordInput())
    email = forms.EmailField(required= False)
