# Generated by Django 5.0.7 on 2024-09-03 16:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0008_fileentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileentry',
            name='VaultEntry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='vault.vaultentry'),
        ),
    ]
