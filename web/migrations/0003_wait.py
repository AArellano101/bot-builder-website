# Generated by Django 3.1.7 on 2021-05-30 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_loop'),
    ]

    operations = [
        migrations.CreateModel(
            name='wait',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot_id', models.IntegerField(default=-1)),
                ('milliseconds', models.IntegerField(default=0)),
            ],
        ),
    ]
