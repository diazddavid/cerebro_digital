# Generated by Django 3.2.15 on 2022-09-26 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notasPensamiento', '0012_auto_20220919_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='extracto',
            name='en_aleatorio',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='zettelcasten',
            name='en_aleatorio',
            field=models.BooleanField(default=False),
        ),
    ]
