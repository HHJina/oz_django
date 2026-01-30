# todo / cb_urls.py

from django.urls import path
from todo_list import views

app_name = 'fb'

urlpatterns = [
    path('', views.todo_list, name='list'),
    path('<int:todo_id>/', views.todo_info, name='info'),
    path('create/', views.todo_create, name='create'),
    path('<int:todo_id>/update/', views.todo_update, name="update"),
    path('<int:todo_id>/delete/', views.todo_delete, name="delete"),
]