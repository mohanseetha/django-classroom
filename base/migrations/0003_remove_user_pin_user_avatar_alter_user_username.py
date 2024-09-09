# Generated by Django 5.1 on 2024-09-09 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_user_email_alter_user_name_alter_user_pin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='pin',
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='avatar.svg', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
