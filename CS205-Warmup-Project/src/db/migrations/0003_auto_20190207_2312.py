# Generated by Django 2.1.5 on 2019-02-08 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0002_auto_20190206_0217'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='listing',
            unique_together={('street', 'price', 'type')},
        ),
    ]