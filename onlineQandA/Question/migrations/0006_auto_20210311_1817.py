# Generated by Django 2.2.13 on 2021-03-11 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Question', '0005_auto_20210311_1648'),
    ]

    operations = [
        migrations.CreateModel(
            name='IpModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='views',
            field=models.ManyToManyField(blank=True, related_name='ans_views', to='Question.IpModel'),
        ),
        migrations.AddField(
            model_name='question',
            name='views',
            field=models.ManyToManyField(blank=True, related_name='que_views', to='Question.IpModel'),
        ),
    ]
