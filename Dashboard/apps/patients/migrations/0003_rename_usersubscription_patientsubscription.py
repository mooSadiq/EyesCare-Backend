# Generated by Django 5.0.6 on 2024-09-27 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_subscriptionplan_usersubscription'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserSubscription',
            new_name='PatientSubscription',
        ),
    ]
