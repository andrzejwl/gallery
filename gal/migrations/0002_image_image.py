# Generated by Django 3.0.6 on 2020-06-03 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='image',
            field=models.ImageField(default='sample.jpg', upload_to='images'),
        ),
    ]