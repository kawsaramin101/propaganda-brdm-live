# Generated by Django 3.2 on 2021-05-04 07:06

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0006_auto_20210504_1304'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CommentReplies',
            new_name='CommentReply',
        ),
    ]
