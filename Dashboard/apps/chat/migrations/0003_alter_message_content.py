# Generated by Django 5.0.6 on 2024-09-14 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_message_is_read_message_is_received_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(null=True),
        ),
    ]
