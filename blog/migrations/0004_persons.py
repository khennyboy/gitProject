# Generated by Django 5.1 on 2024-09-28 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_remove_memberships_group_remove_memberships_person_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
    ]
