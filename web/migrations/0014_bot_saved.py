# Generated by Django 3.1.7 on 2021-06-10 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_bot_failsafe'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot',
            name='saved',
            field=models.BooleanField(default=False),
        ),
    ]
