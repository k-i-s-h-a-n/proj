# Generated by Django 4.2 on 2023-05-08 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Teachers', '0008_examscore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examscore',
            name='classes',
            field=models.CharField(max_length=500),
        ),
    ]
