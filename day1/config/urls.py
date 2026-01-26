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
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import path

game_list = [
    {'title' : '33원정대', 'grade' : 1},
    {'title' : '킹덤컴', 'grade' : 2},
    {'title' : '데스 스트랜딩2', 'grade' : 3},
    {'title' : '하데스2', 'grade' : 4},
    {'title' : '고스트 오브 요테이', 'grade' : 5},
    {'title' : '할로우 나이트 실크송', 'grade' : 6}
]

def index(request):
    return HttpResponse("<h1>Hello World!</h1>")

def book_list(request):
    # book_text = ''
    #
    # for v in range(1,11):
    #     book_text += f'book{v}<br>'

    return render(request,'book_list.html', {'book_list':book_list, 'range': range(0,10)})

def book(request, num):
    # book_text = f'book {num}번 페이지입니다'
    return render(request,'book_detail.html',{'num':num})

def language(request,lang):
    return HttpResponse(f'<h1>{lang}</h1>')

def games(request):
    # game_titles = [f'<a href="/game/{idx}">{game["title"]}</a><br>' for idx,game in enumerate(game_list)]

    # game_titles = []
    # for game in game_list:
    #     game_titles.append(game['title'])

    # response_text = '<br>'.join(game_titles)
    # return HttpResponse(response_text)

    return render(request, 'games.html', {'game_list':game_list})

def game_detail(request, index):
    if index > len(game_list) - 1:
        raise Http404

    game = game_list[index]
    context = {'game':game, 'index':index}
    return render(request, 'game.html', context)

def gugu(request,num):
    if num < 2:
        return redirect('/gugu/2')

    gugu_list = []
    for i in range(1,11):
        result = num * i
        gugu_list.append(result)

    context = {
        'gugu_list':gugu_list,
        'num':num,
        'range':range(0,10)}
    return render(request,'gugu.html',context)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    path('book_list/',book_list),
    path('book_list/<int:num>',book),
    path('language/<str:lang>',language),
    path('game/',games),
    path('game/<int:index>',game_detail),
    path('gugu/<int:num>',gugu),
]
