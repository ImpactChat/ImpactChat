# Generated by Django 3.1 on 2020-08-21 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impactadmin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.CharField(default='U', max_length=1),
        ),
    ]
