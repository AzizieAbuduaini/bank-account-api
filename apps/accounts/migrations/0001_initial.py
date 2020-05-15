# Generated by Django 2.2.10 on 2020-05-14 17:08

import apps.accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_modified_timestamp', models.DateTimeField(auto_now_add=True)),
                ('account', models.IntegerField()),
                ('balance', models.DecimalField(decimal_places=4, max_digits=20)),
                ('name', models.CharField(max_length=128)),
                ('is_active', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_account', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_account',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_modified_timestamp', models.DateTimeField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=4, max_digits=20)),
                ('status', enumfields.fields.EnumField(enum=apps.accounts.models.TransactionStatuses, max_length=10)),
                ('type', enumfields.fields.EnumField(enum=apps.accounts.models.TransactionTypes, max_length=10)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'trnasactions',
            },
        ),
    ]