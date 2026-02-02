# todo / cb_urls.py

from django.urls import path
from todo_list import cb_views

app_name = 'todo'

urlpatterns = [
    path('', cb_views.TodoListView.as_view(), name='list'),
    path('create/', cb_views.TodoCreateView.as_view(), name='create'),
    path('<int:todo_id>/', cb_views.TodoDetailView.as_view(), name='info'),
    path('<int:pk>/update/', cb_views.TodoUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', cb_views.TodoDeleteView.as_view(), name='delete'),

    # comment
    path('comment/<int:todo_id>/create/',  cb_views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete/',  cb_views.CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:pk>/update/', cb_views.CommentUpdateView.as_view(), name='comment_update'),
]