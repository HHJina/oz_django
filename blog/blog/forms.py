from django import forms
from .models import Blog

# 모델폼을 자동으로 읽어서 입력창을 자동으로 그려줌
class BlogForm(forms.ModelForm): # Model을 가지고 만들어서 ModelForm 상속
    class Meta:
        model = Blog
        fields = ('category','title', 'content', )
