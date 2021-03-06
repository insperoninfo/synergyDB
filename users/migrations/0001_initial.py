# Generated by Django 2.2 on 2021-04-01 03:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=30)),
                ('gender', models.CharField(choices=[('male', 'M'), ('Female', 'F'), ('Other', 'O')], max_length=15)),
                ('branch', models.CharField(choices=[('Kathmandu', 'KTM'), ('Bhaktapur', 'BTP')], max_length=50)),
                ('phone', models.PositiveIntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
