# Generated by Django 2.1.7 on 2019-04-06 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0004_auto_20190328_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicinesupply',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='resources',
            field=models.IntegerField(default=0),
        ),
    ]