# Generated by Django 5.0.7 on 2024-09-03 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vault', '0009_alter_fileentry_vaultentry'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileentry',
            name='iv',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
