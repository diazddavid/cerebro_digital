# Generated by Django 3.2.15 on 2022-09-11 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notasPensamiento', '0006_referencia_en_bibliografia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extracto',
            name='pensar',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
