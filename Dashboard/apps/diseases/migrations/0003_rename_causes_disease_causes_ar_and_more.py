# Generated by Django 5.0.6 on 2024-09-11 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diseases', '0002_disease_created_at_disease_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='disease',
            old_name='causes',
            new_name='causes_ar',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='description',
            new_name='description_ar',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='diagnosis_methods',
            new_name='diagnosis_methods_ar',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='name',
            new_name='name_ar',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='prevention_recommendations',
            new_name='prevention_recommendations_ar',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='symptoms',
            new_name='symptoms_ar',
        ),
        migrations.RenameField(
            model_name='disease',
            old_name='treatment_options',
            new_name='treatment_options_ar',
        ),
        migrations.AddField(
            model_name='disease',
            name='causes_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='disease',
            name='description_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='disease',
            name='diagnosis_methods_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='disease',
            name='name_en',
            field=models.CharField(default='null', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='disease',
            name='prevention_recommendations_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='disease',
            name='symptoms_en',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='disease',
            name='treatment_options_en',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='disease',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]