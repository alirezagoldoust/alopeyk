# Generated by Django 4.2 on 2024-01-09 14:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_profile_phone_numer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='phone_numer',
            new_name='phone_number',
        ),
    ]