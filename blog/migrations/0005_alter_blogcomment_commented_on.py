# Generated by Django 3.2 on 2021-04-30 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20210430_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogcomment',
            name='commented_on',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='blog.blogpost'),
        ),
    ]
