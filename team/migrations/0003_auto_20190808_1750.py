# Generated by Django 2.2.4 on 2019-08-08 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0002_auto_20190806_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='password',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]