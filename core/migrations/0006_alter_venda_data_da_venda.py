# Generated by Django 4.1.6 on 2023-02-26 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_venda_data_da_venda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='data_da_venda',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]