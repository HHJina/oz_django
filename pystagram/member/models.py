from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('올바른 이메일을 입력하세요.')

        # 이메일을 정규화하여 유저 객체 생성
        user = self.model(
            email=self.normalize_email(email),
        )
        # 비밀번호 해싱
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        verbose_name='email',
        unique=True
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    nickname = models.CharField('nickname', max_length=20, unique=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    # 관리자 페이지나 시스템 내에서 필요한 설정들
    class Meta:
        verbose_name = '유저'
        verbose_name_plural = f'{verbose_name} 목록'

    def get_full_name(self):
        return self.nickname
    def get_short_name(self):
        return self.nickname

    def __str__(self):
        return self.nickname
    # 특정권한이 있는지 확인하는 메서드
    def has_perm(self, perm, obj=None):
        return True
    # 특정 앱의 모델에 접 권한이 있는지 확인
    def has_module_perms(self, app_label):
        return True
    # 관리자 페이지에 로그인 여부를 is_admin으로 판단
    @property
    def is_staff(self):
        return self.is_admin
    # 슈퍼유저인지 is_admin으로 판단
    @property
    def is_superuser(self):
        return self.is_admin


