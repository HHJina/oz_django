from django.db import models


class TimestampModel(models.Model):
    created_at = models.DateTimeField('생성일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)

    class Meta:
        # 실제DB테이블로 만들지말고 부모역할로만 쓴다
        abstract = True