"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from django.views import View

from blog.views import blog_list, blog_detail, blog_create, blog_update, blog_delete
from blog import cb_views
from member.views import signup, login


class AboutView(TemplateView):
    template_name = 'about.html'

class TestView(View): # Django의 View 클래스 상속
    def get(self, request):
        return render(request, 'test_get.html')

    def post(self, request):
        return render(request, 'test_post.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fb/', include('blog.fbv_urls')), # function based view include
    path('', include('blog.urls')), # class based view include

    # auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),

    # CBV
    path('about', AboutView.as_view(), name='about'),
    path('redirect/', RedirectView.as_view(pattern_name='about'), name='redirect'),
    path('test/', TestView.as_view(), name='test'),
    # path('redirect2/', lambda req: redirect('about')),

]
