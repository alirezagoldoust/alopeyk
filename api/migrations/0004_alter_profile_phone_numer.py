# Generated by Django 4.2 on 2024-01-09 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_profile_phone_numer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_numer',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
