# Generated by Django 3.2.4 on 2021-08-10 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_bloguser_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to='users_images/'),
        ),
    ]