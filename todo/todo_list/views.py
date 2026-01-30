# views.py
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse

# from .models import TodoList
from todo_list.models import TodoList
from .forms import TodoForm, TodoUpdateForm

@login_required()
def todo_list(request):
    todo_list = TodoList.objects.filter(user=request.user).order_by('-start_date')
    # 검색
    q = request.GET.get('q')
    if q:
        todo_list = todo_list.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    # 페이지네이션
    paginator = Paginator(todo_list, 10)
    page_number = request.GET.get('page')
    # 페이지 자륵디
    page_object = paginator.get_page(page_number)

    context = {
        'page_obj' : page_object,
    }

    return render(request, 'todo_list.html', context)


@login_required()
def todo_info(request, todo_id):
    try:
        # todo = TodoList.objects.get(id=todo_id)
        todo = get_object_or_404(TodoList, pk=todo_id)
        todo = model_to_dict(todo)
        # todo = todo.__dict__

        # info = {
        #     'id': todo_id,
        #     'title': todo.title,
        #     'description': todo.description,
        #     'start_date': todo.start_date,
        #     'end_date': todo.end_date,
        #     'is_completed': todo.is_completed,
        # }

        context = {
            'todo': todo,
        }
        return render(request, 'todo_info.html', context)
    except TodoList.DoesNotExist:
        raise Http404("Todo does not exist")

def todo_create(request):
    form = TodoForm(request.POST or None)
    if form.is_valid() and request.method == 'POST':
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect(reverse('todo:info', kwargs={'todo_id': todo.id}))
    else:
        form = TodoForm()

    context = {
        'form': form
    }
    return render(request, 'todo_create.html', context)

def todo_update(request, todo_id):
    todo = get_object_or_404(TodoList, id=todo_id, user=request.user)
    form = TodoUpdateForm(request.POST or None, instance=todo)
    if form.is_valid():
        form.save()
        return redirect(reverse('todo:info', kwargs={'todo_id': todo.id}))
    context = {
        'form': form
    }
    return render(request, 'todo_update.html', context)

def todo_delete(request, todo_id):
    todo = get_object_or_404(TodoList, id=todo_id, user=request.user)
    todo.delete()
    return redirect(reverse('todo:list'))