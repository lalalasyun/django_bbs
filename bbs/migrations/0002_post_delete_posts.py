# Generated by Django 4.2.1 on 2023-06-07 01:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bbs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, default=None, editable=False, null=True, verbose_name='deleted date')),
                ('text', models.TextField(verbose_name='テキスト')),
                ('posted_at', models.DateTimeField(auto_now_add=True, verbose_name='投稿日')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='投稿者')),
            ],
            options={
                'db_table': 'post',
            },
        ),
        migrations.DeleteModel(
            name='Posts',
        ),
    ]
