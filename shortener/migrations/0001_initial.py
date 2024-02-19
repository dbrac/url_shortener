# Generated by Django 5.0 on 2023-12-09 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shortener',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.TextField(max_length=1000)),
                ('short_key', models.TextField(max_length=30)),
                ('tags', models.TextField(max_length=100)),
                ('active_duration', models.CharField(choices=[(1, 1), (3, 3), (6, 6), (12, 12)], max_length=2)),
                ('createdDate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
