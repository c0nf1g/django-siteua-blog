# Generated by Django 3.2.4 on 2021-08-10 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_remove_comment_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='header_photo',
            field=models.ImageField(blank=True, null=True, upload_to='posts_images/'),
        ),
    ]