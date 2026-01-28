from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as django_login
from django.shortcuts import render, redirect, reverse
from django.conf import settings
# from blog.config import settings



def signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)

    # if request.method == 'POST':
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/accounts/login/')
    # else:
    #     form = UserCreationForm()

    context = {
        'form' : form,
    }
    return render(request,'registration/signup.html',context)


def login(request):
    form = AuthenticationForm(request,request.POST or None)

    if form.is_valid():
        django_login(request, form.get_user())
        return redirect(reverse('blog_list'))

    context = {
        'form' : form,
    }
    return render(request,'registration/login.html',context)