# Generated by Django 4.2.4 on 2023-09-25 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_illustration_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='illustration',
            name='del_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='illustration',
            name='illu',
            field=models.ImageField(upload_to='illustration'),
        ),
    ]
