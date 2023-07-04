from django.db import models
from django.conf import settings
from django_boost.models.mixins  import LogicalDeletionMixin

# Create your models here.
class Post(LogicalDeletionMixin):
    text = models.TextField("テキスト", blank=False)

    posted_at = models.DateTimeField("投稿日", auto_now_add=True)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name="投稿者",on_delete=models.CASCADE)

    class Meta:
        db_table = "post"

    def __str__(self):
        return f'{self.pk}'
    