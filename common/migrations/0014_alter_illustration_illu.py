# Generated by Django 4.2.4 on 2023-11-10 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_remove_illustration_tag_illustration_feature_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='illustration',
            name='illu',
            field=models.CharField(max_length=200),
        ),
    ]
