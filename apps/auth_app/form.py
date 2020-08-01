from django import forms
from django.contrib.auth.models import User
from apps.utils.form import FormMixin


class SignupForm(forms.ModelForm, FormMixin):
    pwd1 = forms.CharField(min_length=6, error_messages=({'min_length': '请设置6位以上的密码', 'required': '请设置密码'}))
    pwd2 = forms.CharField(min_length=6, error_messages=({'min_length': '', 'required': '请确认密码'}))
    email = forms.EmailField(error_messages=({'required': '请设置邮箱'}))

    class Meta:
        model = User
        fields = ['username']
        error_messages = {
            'username': {
                'required': '请设置用户名',
            }
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        exists = User.objects.filter(username__icontains=username).exists()
        if exists:
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        exists = User.objects.filter(email__icontains=email).exists()
        if exists:
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean(self):
        cleaned_data = super().clean()
        pwd1 = cleaned_data.get('pwd1')
        pwd2 = cleaned_data.get('pwd2')
        if pwd1 != pwd2:
            raise forms.ValidationError('两次输入密码不一致')


class LoginForm(forms.ModelForm, FormMixin):
    remember = forms.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password']


class EditInfoForm(forms.ModelForm, FormMixin):
    user_id = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'email']
        error_messages = {
            'username': {
                'required': '请输入用户名',
            },
            'email': {
                'required': '请输入邮箱'
            }
        }

    def clean(self):
        user_id = self.cleaned_data.get('user_id')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        user = User.objects.get(pk=user_id)
        username_exists = User.objects.filter(username=username).exists()

        # 如果当前登录账号的用户名不等于所输入的用户名，并且所输入的用户名存在，
        # 则提示“用户名已存在”
        if user.username != username and username_exists:
            raise forms.ValidationError('用户名已存在')

        # 如果当前登录账号的邮箱不等于所输入的邮箱，并且所输入的邮箱存在，
        # 则提示“邮箱已存在”
        email_exists = User.objects.filter(email=email).exists()
        if user.email != email and email_exists:
            raise forms.ValidationError('邮箱已存在')


