# Generated by Django 3.2.5 on 2021-08-10 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(default='category.png', upload_to='category/'),
        ),
    ]
