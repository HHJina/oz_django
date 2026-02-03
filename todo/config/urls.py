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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from todo_list import views
from users import views as user_views
# from ..todo_list import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.todo_list, name='todo_list'),
    # path('<int:todo_id>/', views.todo_info, name='todo_info'),
    # path('create/', views.todo_create, name='todo_create'),
    # path('<int:todo_id>/update/', views.todo_update, name="todo_update"),
    # path('<int:todo_id>/delete/', views.todo_delete, name="todo_delete"),

    # FBV URL include
    path('fb/', include('todo_list.fb_urls')),
    # CBV URL include
    path('', include('todo_list.cb_urls')),

    # user
    path('accounts/', include('django.contrib.auth.urls')), # django 기본 로그인 기능
    path('signup/', user_views.signup, name='signup'),
    path('login/', user_views.login, name='login'), # 직접 만든 로그인 기증

    # summernote
    path('summernote/', include('django_summernote.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
