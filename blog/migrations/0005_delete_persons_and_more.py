# Generated by Django 5.1 on 2024-09-29 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_persons'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Persons',
        ),
        migrations.RemoveIndex(
            model_name='post',
            name='blog_post_publish_bb7600_idx',
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('DF', 'Draft'), ('PB', 'Published')], default='PB', max_length=2),
        ),
    ]
