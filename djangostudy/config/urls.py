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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from posts.views import PostViewSet  # posts 앱의 ViewSet 임포트
from comments.views import CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')  # basename 지정 베스트 프랙티스
router.register(r'comments', CommentViewSet, basename='comment') # api호출을 위해 설정

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),  # 세션 1에서 추가된 부분 유지
    path('api/', include(router.urls)),  # router URL 통합, 모듈화 베스트 프랙티스
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # access 토큰 가져옴
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refresh 토큰 가져옴
]


# 이후 ViewSet 추가 시 router 사용 예시
# router = DefaultRouter()
# urlpatterns += router.urls
