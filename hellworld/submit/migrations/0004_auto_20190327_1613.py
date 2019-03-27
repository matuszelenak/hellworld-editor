# Generated by Django 2.1.7 on 2019-03-27 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0003_auto_20190327_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='submitscore',
            name='compilation_message',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='submit',
            name='status',
            field=models.IntegerField(choices=[(0, 'Waiting'), (1, 'Running'), (2, 'OK'), (3, 'WA'), (4, 'Compilation error'), (5, 'Runtime exception')], default=0),
        ),
    ]