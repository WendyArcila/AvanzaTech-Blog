# Generated by Django 5.0.4 on 2024-04-06 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_post', '0002_blogpost_updated_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='excerpt',
        ),
    ]
