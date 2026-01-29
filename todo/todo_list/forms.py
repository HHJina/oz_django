from django import forms

from .models import TodoList

# 모델폼을 자동으로 읽어서 입력창을 자동으로 그려줌
class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['title', 'description', 'start_date', 'end_date']

        # 날짜부분 위젯 추가
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ('title', 'description', 'is_completed')
