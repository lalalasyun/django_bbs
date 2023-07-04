from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import MinLengthValidator,RegexValidator
from django_boost.models.mixins  import LogicalDeletionMixin
from django.utils.text import slugify

import uuid,os

from django_bbs import settings

def get_image_path(self,filename):
    """カスタマイズした画像パスを取得する.

    :param self: インスタンス (models.Model)
    :param filename: 元ファイル名
    :return: カスタマイズしたファイル名を含む画像パス
    """
    prefix = 'images/'
    name = str(uuid.uuid4()).replace('-', '')
    extension = os.path.splitext(filename)[-1]
    return prefix + name + extension

class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user
    
class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='ユーザID', max_length=10, unique=True, validators=[MinLengthValidator(5,), RegexValidator(r'^[a-zA-Z0-9]*$',)])
    nickname = models.CharField(verbose_name='ニックネーム', max_length=10, blank=False, null=False)
    date_of_birth = models.DateField(verbose_name="誕生日", blank=True, null=True)
    image = models.ImageField(verbose_name='プロフィール画像', upload_to=get_image_path, blank=True, null=True)
    introduction = models.TextField(verbose_name='自己紹介', max_length=300, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='登録日', auto_now_add=True)
    
    view_timeline = models.CharField(verbose_name='タイムライン表示設定', max_length=10, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    #AbstractBaseUserにはMyUserManagerが必要
    objects = MyUserManager()
    #一意の識別子として使用されます
    USERNAME_FIELD = 'username'
    #ユーザーを作成するときにプロンプ​​トに表示されるフィールド名のリストです。
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
class Follow(models.Model):
    followed_to = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = "フォローされた人", on_delete = models.CASCADE,related_name="followed_to")
    followed_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = "フォローする人", on_delete = models.CASCADE,related_name="followed_by")

    followed_at = models.DateTimeField("フォロー日", auto_now_add=True)

    class Meta:
        db_table = "follow"