# Generated by Django 3.2.16 on 2024-06-23 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0016_auto_20240623_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_attempts',
            field=models.IntegerField(default=0),
        ),
    ]
