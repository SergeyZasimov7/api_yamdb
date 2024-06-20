from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=6),
        ),
    ]
