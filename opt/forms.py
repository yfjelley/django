from form.forms import ContactForm
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = form.CharField(label='密码',widget=forms.PasswordInput())
