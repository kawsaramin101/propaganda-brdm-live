# Generated by Django 3.2 on 2021-04-28 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
