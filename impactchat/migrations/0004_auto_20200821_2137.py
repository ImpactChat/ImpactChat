# Generated by Django 3.1 on 2020-08-21 21:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('impactchat', '0003_auto_20200821_2046'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='channel',
            options={'permissions': [('read_channel', 'Can see the channel and read it'), ('write_channel', 'Can write in the channel')]},
        ),
    ]