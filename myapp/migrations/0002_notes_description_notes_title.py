# Generated by Django 5.0.2 on 2024-03-31 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='description',
            field=models.TextField(default='shruti'),
        ),
        migrations.AddField(
            model_name='notes',
            name='title',
            field=models.CharField(default='shruti', max_length=20),
        ),
    ]