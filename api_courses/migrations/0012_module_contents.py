# Generated by Django 4.2.15 on 2024-08-19 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_courses', '0011_item_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='contents',
            field=models.ManyToManyField(blank=True, to='api_courses.content'),
        ),
    ]
