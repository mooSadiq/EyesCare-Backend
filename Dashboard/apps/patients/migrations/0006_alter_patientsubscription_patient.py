# Generated by Django 5.0.6 on 2024-10-02 20:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0005_patientsubscription_remaining_consultations_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientsubscription',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patient_subscription', to='patients.patient'),
        ),
    ]