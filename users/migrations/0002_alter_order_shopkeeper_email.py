# Generated by Django 4.0.3 on 2022-04-05 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shopkeeper_email',
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]
