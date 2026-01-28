from django.shortcuts import render, get_object_or_404

from .models import Blog


def blog_list(request):
    blog_list = Blog.objects.all()

    # 쿠키 설정
    visits = int(request.COOKIES.get('visits', 0)) + 1
    # 세션 설정
    request.session['count'] = request.session.get('count', 0) + 1

    context = {
        'blog_list': blog_list,
        'count': request.session['count'],
    }

    response = render(request,'blog_list.html', context)

    response.set_cookie('visits',visits)
    return  response

def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    context = {'blog': blog, 'pk':pk}
    return render(request,'blog_detail.html', context)
