# Generated by Django 4.2.13 on 2024-06-28 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_category_event_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='event',
            name='longitude',
        ),
    ]
