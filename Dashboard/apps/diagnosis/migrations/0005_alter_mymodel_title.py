# Generated by Django 5.0.2 on 2024-09-06 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnosis', '0004_alter_diagnosisreport_diagnosis_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mymodel',
            name='title',
            field=models.CharField(max_length=300),
        ),
    ]
