# Generated by Django 4.1.1 on 2023-05-18 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_rename_bdp_hadlock_1_reporte_bpd_hadlock_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='lmp',
            field=models.CharField(blank=True, db_column='LMP', max_length=50, null=True),
        ),
    ]