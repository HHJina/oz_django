# todo/cb_views.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import paginator
from django.http import HttpResponseRedirect, Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.shortcuts import get_object_or_404

from todo_list.forms import TodoForm, TodoUpdateForm, CommentForm
from todo_list.models import TodoList, Comment


class TodoListView(LoginRequiredMixin, ListView):
    queryset = TodoList.objects.all()
    template_name = 'todo_list.html'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        if self.request.user.is_superuser:
            queryset = super().get_queryset()

        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return queryset


class TodoDetailView(LoginRequiredMixin, ListView):
    # model = TodoList
    # queryset = TodoList.objects.all().prefetch_related("comments", "comments__user")
    # template_name = 'todo_info.html'
    model = Comment
    template_name = 'todo_info.html'
    context_object_name = 'comments'
    paginate_by = 10

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset)
    #
    #     if obj.user != self.request.user and not self.request.user.is_superuser:
    #         raise Http404("해당 To Do를 조회할 권한이 없습니다.")
    #     return obj
    def get(self, request, *args, **kwargs):
        self.todo_object = get_object_or_404(TodoList, pk=kwargs.get('todo_id'))

        if self.todo_object.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("조회 권한이 없습니다.")

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Comment.objects.filter(todo=self.todo_object).prefetch_related('user')

    # def get_context_data(self, **kwargs):
    #     context = {
    #         'todo': self.object.__dict__,
    #         'comment': CommentForm(),
    #         'page_obj': paginator.get_page(self.request.GET.get("page")),
    #     }
    #     return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo'] = self.todo_object
        context['comment_form'] = CommentForm()
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = TodoList
    # fields = ['title', 'description', 'start_date', 'end_date']
    form_class = TodoForm # 달력위젯 사용을 위해 폼함수 사용
    template_name = 'todo_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('todo:info', kwargs={'todo_id': self.object.id})


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = TodoList
    # fields = ['title', 'description', 'start_date', 'end_date', 'is_completed', 'id']
    form_class = TodoUpdateForm # 달력위젯 사용을 위해 폼함수 사용
    template_name = 'todo_update.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do를 수정할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('todo:info', kwargs={'todo_id': self.object.id})


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = TodoList

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do를 삭제할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('todo:list')


# comment
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    # fields = ["message"]
    form_class = CommentForm
    # pk_url_kwarg = "todo_id"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.todo = get_object_or_404(TodoList, id=self.kwargs["todo_id"])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("todo:info", kwargs={"todo_id": self.kwargs["todo_id"]})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    # fields = ["message"]
    form_class = CommentForm

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 댓글을 수정할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy("todo:info", kwargs={"todo_id": self.object.todo.id})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 댓글을 삭제할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy("todo:list", kwargs={"todo_id": self.object.todo.id})
