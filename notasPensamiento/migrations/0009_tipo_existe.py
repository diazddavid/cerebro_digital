# Generated by Django 3.2.15 on 2022-09-11 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notasPensamiento', '0008_auto_20220911_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipo',
            name='existe',
            field=models.IntegerField(default=1),
        ),
    ]
