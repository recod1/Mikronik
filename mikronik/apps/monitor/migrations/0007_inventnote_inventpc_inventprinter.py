# Generated by Django 3.2.7 on 2021-10-18 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0006_auto_20210914_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostNameNote', models.CharField(max_length=20)),
                ('userNote', models.CharField(max_length=50)),
                ('modelNote', models.CharField(max_length=50)),
                ('hardDriveNote', models.CharField(max_length=20)),
                ('ramNote', models.CharField(max_length=20)),
                ('processorNote', models.CharField(max_length=50)),
                ('placeNote', models.CharField(max_length=20)),
                ('dateInvent', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='InventPC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostNamePC', models.CharField(max_length=20)),
                ('userPC', models.CharField(max_length=50)),
                ('motherBandPC', models.CharField(max_length=50)),
                ('hardDrivePC', models.CharField(max_length=20)),
                ('ramPC', models.CharField(max_length=20)),
                ('processorPC', models.CharField(max_length=50)),
                ('placePC', models.CharField(max_length=20)),
                ('dateInvent', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='InventPrinter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostNamePrinter', models.CharField(max_length=20)),
                ('modelPrinter', models.CharField(max_length=50)),
                ('tonerTypePrinter', models.CharField(max_length=20)),
                ('placePrinter', models.CharField(max_length=20)),
                ('dateInvent', models.CharField(max_length=20)),
            ],
        ),
    ]
