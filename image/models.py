import os
import hashlib
from django.db import models
from datetime import datetime
from accounts.models import  MyUser

from django.core.validators import MaxValueValidator, MinValueValidator

def upload_to_uuid(instance, filename):
    current_time = datetime.now()
    pre_hash_name = '%s%s%s' % (instance.pk, filename, current_time)
    hs_filename = '%s.%s' % (hashlib.md5(pre_hash_name.encode()).hexdigest(), 'webp')
    return '%s%s' % ('images/upload/', hs_filename)


# Create your models here.
class UploadImage(models.Model):
    image = models.ImageField(upload_to = upload_to_uuid)
    trim_image = models.ImageField(upload_to = 'images/user', blank=True)

    upload_by = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='trim_image')

    is_edited = models.BooleanField(default=False, blank=True)
    position_x = models.IntegerField(default=0, blank=True)
    position_y = models.IntegerField(default=0, blank=True)
    zoom = models.IntegerField(default=0, blank=True, validators=[MinValueValidator(0),MaxValueValidator(100)])

    class Meta:
        db_table = 'upload_image'
        
