# Generated by Django 4.0.6 on 2022-07-29 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userID', models.CharField(max_length=20, unique=True)),
                ('userPicUrl', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
