# Generated by Django 2.2 on 2019-05-11 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pandemic', '0003_auto_20190511_1153'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='logged_in',
        ),
        migrations.AlterField(
            model_name='bluetoothtag',
            name='address',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='medicinesupply',
            unique_together={('medicine', 'team')},
        ),
    ]
