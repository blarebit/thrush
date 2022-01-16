# Generated by Django 4.0.1 on 2022-01-16 15:25

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('price', models.PositiveIntegerField()),
                ('discount', models.PositiveSmallIntegerField(default=0)),
                ('start', models.DateTimeField(blank=True, default=datetime.datetime(2022, 1, 16, 15, 25, 46, 811263), null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['created_at'],
                'abstract': False,
            },
        ),
    ]
