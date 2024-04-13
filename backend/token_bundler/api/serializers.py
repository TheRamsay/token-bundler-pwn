from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Asset, WalletAsset, Bundle, BundleAsset

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'name', 'symbol', 'decimals', 'address', 'total_supply', 'asset_type', 'token_id']


class WalletAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletAsset
        fields = ['user_wallet', 'asset', 'balance']
        # Join nested fields
        depth = 1

class BundleAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundleAsset
        fields = ['bundle', 'asset', 'balance']
        depth = 1

    
class SimpleBundleAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundleAsset
        fields = ['asset', 'balance']
        depth = 1

class BundleSerializer(serializers.ModelSerializer):
    bundle_assets = SimpleBundleAssetSerializer(many=True, read_only=True, source='bundleasset_set')

    class Meta:
        model = Bundle
        fields = ['bundle_id', 'address', 'bundle_assets']
        depth = 1