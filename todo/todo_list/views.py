# views.py

from django.http import Http404
from django.shortcuts import render
# from .models import TodoList
from todo_list.models import TodoList

def todo_list(request):
    todo_list = TodoList.objects.all().values_list('id', 'title')
    result = [{'id': todo[0], 'title': todo[1]} for todo in todo_list]

    return render(request, 'todo_list.html', {'data': result})


def todo_info(request, todo_id):
    try:
        todo = TodoList.objects.get(id=todo_id)
        info = {
            'title': todo.title,
            'description': todo.description,
            'start_date': todo.start_date,
            'end_date': todo.end_date,
            'is_completed': todo.is_completed,
        }
        return render(request, 'todo_info.html', {'data': info})
    except TodoList.DoesNotExist:
        raise Http404("Todo does not exist")