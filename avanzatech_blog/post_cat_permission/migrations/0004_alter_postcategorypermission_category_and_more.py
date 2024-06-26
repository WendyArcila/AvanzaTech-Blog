# Generated by Django 5.0.3 on 2024-03-08 18:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('permission', '0001_initial'),
        ('post_cat_permission', '0003_alter_postcategorypermission_blog_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcategorypermission',
            name='category',
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to='category.category'),
        ),
        migrations.AlterField(
            model_name='postcategorypermission',
            name='permission',
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to='permission.permission'),
        ),
    ]
