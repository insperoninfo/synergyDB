# Generated by Django 2.2 on 2021-05-02 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210425_0213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directory',
            name='branch',
            field=models.CharField(choices=[('Kathmandu', 'KTM'), ('Bhaktapur', 'BTP')], max_length=56),
        ),
    ]