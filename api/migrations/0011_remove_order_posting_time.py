# Generated by Django 4.2 on 2024-01-10 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_order_posting_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='posting_time',
        ),
    ]
