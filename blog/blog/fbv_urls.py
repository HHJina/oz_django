from django.urls import path, include

from blog.views import blog_list,blog_detail,blog_create,blog_update,blog_delete

app_name = 'fb'

urlpatterns = [
    # FBV blog
    path('', blog_list, name='list'),
    path('<int:pk>/', blog_detail, name = 'detail'),
    path('create/',blog_create, name = 'create'),
    path('<int:pk>/update/',blog_update, name = 'update'),
    path('<int:pk>/delete/', blog_delete, name='delete'),
]