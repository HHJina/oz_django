from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods


from .forms import BlogForm
from .models import Blog


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')

    # 검색필터
    q = request.GET.get('q')
    if q:
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )
        # blogs = blogs.filter(title__icontains=q)

    # 페이지네이션
    paginator = Paginator(blogs,10)
    page = request.GET.get('page')
    # 페이지 자르기
    page_object = paginator.get_page(page)

    # 쿠키 설정
    visits = int(request.COOKIES.get('visits', 0)) + 1
    # 세션 설정
    request.session['count'] = request.session.get('count', 0) + 1

    context = {
        # 'blogs': blogs,
        'count': request.session['count'],
        'page_object': page_object,
    }

    print(f"-------{page_object}")
    response = render(request,'blog_list.html', context)

    response.set_cookie('visits',visits)
    return  response

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    context = {'blog': blog, 'pk':pk}
    return render(request,'blog_detail.html', context)

@login_required() # LOGIN_URL로 이동
def blog_create(request):
    # if not request.user.is_authenticated:
    #     return redirect(reverse('login'))

    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect(reverse('blog_detail',kwargs={'pk':blog.id}))
    else:
        form = BlogForm()

    context = {
        'form': form,
    }
    return render(request, 'blog_create.html', context)

def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    # if request.user != blog.author:
    #     raise Http404

    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        form.save()
        return redirect(reverse('blog_detail',kwargs={'pk':blog.id}))

    context = {
        'blog': blog,
        'form': form,
    }

    return render(request, 'blog_update.html', context)


# POST이외의 요청은 거절하기
@require_http_methods(['POST'])
def blog_delete(request, pk):
    # if request.method != 'POST':
    #     return Http404
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog.delete()

    return redirect(reverse('blog_list'))