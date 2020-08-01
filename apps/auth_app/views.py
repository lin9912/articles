from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
# 自定义
from .form import SignupForm, LoginForm, EditInfoForm


class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')

            # 能跑就行...
            try:
                username = User.objects.get(email=email).username
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    if remember:
                        request.session.set_expiry(None)
                    else:
                        request.session.set_expiry(0)
                    return redirect(reverse('auth_app:user_center', kwargs={'username': username}))
                else:
                    errors = form.get_errors()
                    errors.append('邮箱或密码错误')
                    return render(request, 'auth/login.html', context={"errors": errors})
            except:
                errors = form.get_errors()
                errors.append('邮箱或密码错误')
                return render(request, 'auth/login.html', context={"errors": errors})
        else:
            errors = form.get_errors()
            return render(request, 'auth/login.html', context={'errors': errors})


class SignupView(View):
    def get(self, request):
        return render(request, 'auth/signup.html')

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            pwd1 = form.cleaned_data.get('pwd1')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            user = User.objects.create_user(username=username, email=email, password=pwd1)
            login(request, user)
            return redirect(reverse('auth_app:user_center', kwargs={'username': username}))
        else:
            errors = form.get_errors()
            return render(request, 'auth/signup.html', context={'errors': errors})


@login_required(login_url='/login/')
def user_center(request, username):
    if username != request.user.username:
        raise Http404
    else:
        user = User.objects.get(username__icontains=username)
        print()
        context = {
            'user': user,
            'article': request.user.news_set.all(),
        }
        return render(request, 'auth/user_center.html', context=context)


def user_logout(request):
    logout(request)
    return redirect(reverse('news_app:index'))


@login_required(login_url='/login/')
def edit_info(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'GET':
        context = {
            'user': user,
        }
        return render(request, 'auth/edit_info.html', context=context)

    else:
        form = EditInfoForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data.get('user_id')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            user.username = username
            user.email = email
            user.save()
            return redirect(reverse('auth_app:user_center', kwargs={'username': username}))
        else:
            errors = form.get_errors()
            context = {
                'errors': errors,
            }

        return render(request, 'auth/edit_info.html', context=context)
