# Generated by Django 4.2.20 on 2025-05-25 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_studentextra_cl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentextra',
            name='cl',
            field=models.CharField(choices=[('Bsc.Physics', 'Bsc.Physics'), ('Bsc.Chemistry', 'Bsc.Chemistry'), ('Bsc.Bottany', 'Bsc.Bottany'), ('Bsc.Zoology', 'Bsc.Zoology'), ('Bsc.Mathmatics', 'Bsc.Mathmatics'), ('Bsc.Electronics', 'Bsc.Electronics')], max_length=30),
        ),
    ]
