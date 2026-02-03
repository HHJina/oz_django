from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from pathlib import Path
from io import BytesIO

from utils.models import TimestampModel


class TodoList(TimestampModel):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    # 이미지경로
    completed_image = models.ImageField('이미지',null=True, blank=True, upload_to='todo/%Y/%m/%d')
    # 썸네일경로
    thumbnail = models.ImageField('썸네일', null=True, blank=True, upload_to='todo/%Y/%m/%d/thumbnail', default='no_image/image.png')

    # 사용자 추가
    # models.CASCADE => 같이 삭제
    # models.PROTECT => 삭제가 불가능함 (유저를 삭제하려고할때 블로그가 있으면 유저 삭제가 불가능)
    # models.SET_NULL => null값을 넣습니다. => 유저 삭제시 블로그의 author가 null이 됨, 이 때 null=True 옵션도 함께 설정 필요
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    # save함수 오버라이딩
    def save(self,*args,**kwargs):
        if not self.completed_image:
            # 이미지파일이 없을경우 일반저장 진행
            return super().save(*args,**kwargs)

        image = Image.open(self.completed_image)
        image.thumbnail((150,150))

        # Path객체로 변환
        image_path = Path(self.completed_image.name)

        # 이미지의 경로를 이름, 확장자로 뽑음
        thumbnail_name = image_path.stem # /todo/2026/02/03/thumbnail.png => thumbnail
        thumbnail_extension = image_path.suffix # /todo/2026/02/03/thumbnail.png => .png
        thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}'

        # 데이터 저장시 타입을 지정해준다
        if thumbnail_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        else:
            return super().save(*args,**kwargs)

        # 실제 하드디스크가 아닌 임시저장소(ram)를 연다
        temp_thumb = BytesIO()
        # 임시저장소에 저장
        image.save(temp_thumb, file_type)
        # 데이터를 다시 읽기위해 앞으로 이동
        temp_thumb.seek(0)

        # thumbnail 컬럼에 임시저장소 데이터를 할당(아직저장X)
        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        # 임시저장소 폐쇄
        temp_thumb.close()
        # 이제 저장
        return super().save(*args,**kwargs)

class Comment(TimestampModel):
    # blog
    # 댓글 내용
    # 작성자
    # 작성일자
    # 수정일자
    # related_name은 역참조
    todo = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name='comments')
    message = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f'{self.user}: {self.message}'
