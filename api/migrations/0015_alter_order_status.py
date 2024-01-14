# Generated by Django 4.2 on 2024-01-14 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('0', 'initial'), ('1', 'driver accepted'), ('2', 'driver arrived to origin and recieved the box'), ('3', 'delivered'), ('-1', 'canceled from user'), ('-2', 'canceled from driver')], default='0', max_length=20),
        ),
    ]