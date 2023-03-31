# Generated by Django 4.1.7 on 2023-03-31 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombrehospital', models.CharField(max_length=150)),
                ('ciudad', models.CharField(max_length=150)),
                ('departamento', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name_plural': 'Hospitales',
                'db_table': 'Hospital',
                'ordering': ['nombrehospital'],
            },
        ),
        migrations.CreateModel(
            name='Personalsalud',
            fields=[
                ('cedulamed', models.IntegerField(primary_key=True, serialize=False)),
                ('nombresmed', models.CharField(max_length=150)),
                ('apellidosmed', models.CharField(max_length=150)),
                ('telefonomed', models.CharField(max_length=50, unique=True)),
                ('direccionmed', models.CharField(max_length=200)),
                ('hospitalid', models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='main.hospital', verbose_name='Hospitales')),
            ],
            options={
                'verbose_name_plural': 'Personal',
                'db_table': 'PersonalSalud',
                'ordering': ['cedulamed'],
            },
        ),
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('consultaid', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_consulta', models.DateTimeField()),
                ('motivo_consulta', models.CharField(default='Ultrasonido de control', max_length=100)),
                ('txtresults', models.CharField(blank=True, max_length=100, null=True)),
                ('medUltrasonido', models.CharField(blank=True, max_length=200, null=True)),
                ('idfeto', models.IntegerField(blank=True, null=True)),
                ('medConsulta', models.ForeignKey(default='', on_delete=django.db.models.deletion.SET_DEFAULT, to='main.personalsalud')),
            ],
            options={
                'verbose_name_plural': 'Consultas',
                'db_table': 'Consulta',
                'ordering': ['consultaid'],
            },
        ),
    ]
