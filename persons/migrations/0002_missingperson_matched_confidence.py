# Generated by Django 4.0.4 on 2023-03-09 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='missingperson',
            name='matched_confidence',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Details of the Match'),
        ),
    ]
