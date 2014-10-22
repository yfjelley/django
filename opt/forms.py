# -*- coding:utf-8 -*-
from django import forms
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import logging
logger = logging.getLogger("django")
class UserForm(forms.Form):
    userName = forms.CharField(label='用户名',max_length=100)
    userPassword = forms.CharField(label='密码',widget=forms.PasswordInput())
    userPasswordAgain = forms.CharField(label='确认密码',widget=forms.PasswordInput())
    userEmail = forms.EmailField(required= False)
    def clean_password(self):
        userPassword = self.cleaned_data.get('userPassword')
        userPasswordAgain = self.cleaned_data.get('userPasswordAgain')
        logger.info("%s"%userPassword)
        logger.info("%s"%userPasswordAgain)
        if userPassword != userPasswordAgain :
            raise forms.ValidationError("two password is not same!")
        return True 
