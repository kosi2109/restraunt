# Generated by Django 3.2.5 on 2021-08-13 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0010_auto_20210813_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]