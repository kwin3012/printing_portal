# Generated by Django 4.0.3 on 2022-04-11 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_order_shopkeeper_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='printing_status',
            field=models.BooleanField(default=False),
        ),
    ]
