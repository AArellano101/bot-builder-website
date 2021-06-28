# Generated by Django 3.1.7 on 2021-06-01 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_delete_bot'),
    ]

    operations = [
        migrations.CreateModel(
            name='bot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('image', models.CharField(max_length=100000)),
                ('description', models.CharField(default='', max_length=1000000)),
                ('valid_image', models.BooleanField()),
            ],
        ),
    ]
