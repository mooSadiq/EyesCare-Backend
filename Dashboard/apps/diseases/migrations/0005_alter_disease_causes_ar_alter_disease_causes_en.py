# Generated by Django 5.0.6 on 2024-10-12 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diseases', '0004_alter_disease_causes_ar_alter_disease_causes_en_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disease',
            name='causes_ar',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='disease',
            name='causes_en',
            field=models.TextField(null=True),
        ),
    ]