# Generated by Django 4.2 on 2024-10-15 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='history',
            field=models.ManyToManyField(blank=True, to='api.history'),
        ),
    ]