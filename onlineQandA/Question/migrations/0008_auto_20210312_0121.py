# Generated by Django 2.2.13 on 2021-03-11 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Question', '0007_questioncomment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questioncomment',
            old_name='user',
            new_name='postby',
        ),
    ]
