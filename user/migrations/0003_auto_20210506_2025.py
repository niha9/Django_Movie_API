# Generated by Django 3.1 on 2021-05-06 14:55

from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('user', '0002_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
