# Generated by Django 5.0.2 on 2024-08-27 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0003_advertisement_allowed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='ad_image',
            field=models.ImageField(blank=True, null=True, upload_to='ads/'),
        ),
    ]
