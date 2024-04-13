# Generated by Django 5.0.4 on 2024-04-13 11:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=42)),
                ('name', models.CharField(max_length=100, null=True)),
                ('symbol', models.CharField(max_length=10, null=True)),
                ('decimals', models.IntegerField(default=0)),
                ('total_supply', models.DecimalField(decimal_places=0, max_digits=30)),
                ('token_id', models.CharField(default='0', max_length=100)),
                ('asset_type', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Bundle',
            fields=[
                ('bundle_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=42)),
            ],
        ),
        migrations.CreateModel(
            name='UserWallet',
            fields=[
                ('address', models.CharField(max_length=42, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='BundleAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=0, max_digits=30)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.asset')),
                ('bundle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.bundle')),
            ],
        ),
        migrations.AddField(
            model_name='bundle',
            name='assets',
            field=models.ManyToManyField(through='api.BundleAsset', to='api.asset'),
        ),
        migrations.CreateModel(
            name='WalletAsset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=0, max_digits=30)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.asset')),
                ('user_wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.userwallet')),
            ],
        ),
    ]