# Generated by Django 3.0.6 on 2020-06-11 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gal', '0004_auto_20200611_1241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
