# Generated by Django 5.0 on 2024-01-03 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0002_shortener_expires_alter_shortener_active_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortener',
            name='hits',
            field=models.IntegerField(default=0),
        ),
    ]
