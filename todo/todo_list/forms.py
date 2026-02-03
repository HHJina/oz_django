from django import forms
from django_summernote.widgets import SummernoteWidget

from .models import TodoList, Comment


# 모델폼을 자동으로 읽어서 입력창을 자동으로 그려줌
class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['title', 'description', 'start_date', 'end_date']

        # 날짜부분 위젯 추가
        widgets = {
            'description': SummernoteWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력해주세요.'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['title', 'completed_image', 'description', 'start_date', 'end_date', 'is_completed']

        # 날짜부분 위젯 추가
        widgets = {
            'description': SummernoteWidget(),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력해주세요.'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'completed_image': forms.FileInput(attrs={'class': 'form-control'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message',)

