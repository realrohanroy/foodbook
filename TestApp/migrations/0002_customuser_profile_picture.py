# Generated by Django 4.2.11 on 2025-02-12 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/'),
        ),
    ]
