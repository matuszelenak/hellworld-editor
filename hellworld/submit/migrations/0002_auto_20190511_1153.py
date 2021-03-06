# Generated by Django 2.2 on 2019-05-11 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submit',
            name='status',
            field=models.IntegerField(choices=[(0, 'Waiting'), (1, 'Running'), (2, 'OK'), (3, 'WA'), (4, 'Compilation error'), (5, 'Runtime exception'), (6, 'Time limit exceeded'), (7, 'Scoring of the submit failed')], default=0),
        ),
        migrations.AlterField(
            model_name='task',
            name='assignment',
            field=models.FileField(null=True, upload_to='task_assignments'),
        ),
        migrations.AlterField(
            model_name='task',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
