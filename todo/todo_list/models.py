from django.db import models
from django.contrib.auth.models import User

from utils.models import TimestampModel


class TodoList(TimestampModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    # 사용자 추가
    # models.CASCADE => 같이 삭제
    # models.PROTECT => 삭제가 불가능함 (유저를 삭제하려고할때 블로그가 있으면 유저 삭제가 불가능)
    # models.SET_NULL => null값을 넣습니다. => 유저 삭제시 블로그의 author가 null이 됨, 이 때 null=True 옵션도 함께 설정 필요
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(TimestampModel):
    # blog
    # 댓글 내용
    # 작성자
    # 작성일자
    # 수정일자
    todo = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name='comments')
    message = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.user}: {self.message}'
