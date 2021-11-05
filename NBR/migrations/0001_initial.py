# Generated by Django 3.2.6 on 2021-11-02 16:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='team',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('fullName', models.CharField(max_length=255)),
                ('nickName', models.CharField(max_length=255)),
                ('image', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('firstName', models.CharField(max_length=255)),
                ('lastName', models.CharField(max_length=255)),
                ('height', models.CharField(max_length=255)),
                ('weight', models.CharField(max_length=255)),
                ('nationality', models.CharField(max_length=255)),
                ('dateOfBirth', models.DateField()),
                ('addresseeCity', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='userTeam',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('teamId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NBR.team')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NBR.user')),
            ],
        ),
        migrations.CreateModel(
            name='players',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('firstName', models.CharField(max_length=255)),
                ('lastName', models.CharField(max_length=255)),
                ('height', models.CharField(max_length=255)),
                ('weight', models.CharField(max_length=255)),
                ('nationality', models.CharField(max_length=255)),
                ('dateOfBirth', models.DateField()),
                ('imageURL', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('teamId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NBR.team')),
            ],
        ),
        migrations.CreateModel(
            name='login',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NBR.user')),
            ],
        ),
    ]