# Generated by Django 2.2.10 on 2020-05-14 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200514_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='balance',
            field=models.IntegerField(),
        ),
    ]