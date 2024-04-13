from django.db import models

# Create your models here.

class UserWallet(models.Model):
    address = models.CharField(max_length=42, primary_key=True) 

class Asset(models.Model):
    address = models.CharField(max_length=42)
    name = models.CharField(max_length=100, null=True)
    symbol = models.CharField(max_length=10, null=True)
    decimals = models.IntegerField(default=0)
    total_supply = models.DecimalField(max_digits=30, decimal_places=0)
    token_id = models.CharField(max_length=100, default='0')
    asset_type = models.IntegerField(default=0)

class WalletAsset(models.Model):
    user_wallet = models.ForeignKey(UserWallet, on_delete=models.CASCADE, to_field='address')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, to_field='id')
    balance = models.DecimalField(max_digits=30, decimal_places=0)

class Bundle(models.Model):
    bundle_id = models.CharField(primary_key=True, max_length=100)
    address = models.CharField(max_length=42)
    assets = models.ManyToManyField(Asset, through='BundleAsset')

class BundleAsset(models.Model):
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE, to_field='bundle_id')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, to_field='id')
    balance = models.DecimalField(max_digits=30, decimal_places=0)