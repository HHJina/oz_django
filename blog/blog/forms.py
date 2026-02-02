from django import forms
from .models import Blog, Comment

# 모델폼을 자동으로 읽어서 입력창을 자동으로 그려줌
class BlogForm(forms.ModelForm): # Model을 가지고 만들어서 ModelForm 상속
    class Meta:
        model = Blog
        fields = ('category','title', 'content', )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'}) # 부트스트랩
        }
        labels = {
            'content': '댓글'
        }