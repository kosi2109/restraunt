# Generated by Django 3.2.5 on 2021-08-11 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_orderitem_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='usernew',
            name='is_chef',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usernew',
            name='is_user',
            field=models.BooleanField(default=True),
        ),
    ]