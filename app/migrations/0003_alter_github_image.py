# Generated by Django 4.2.3 on 2023-08-21 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_github_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='github',
            name='image',
            field=models.ImageField(upload_to='uploads/app'),
        ),
    ]