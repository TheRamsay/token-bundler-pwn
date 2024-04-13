from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.views import Response
from token_bundler.settings import API_KEY
import aiohttp
import json

from .serializers import WalletAssetSerializer, BundleSerializer, BundleAssetSerializer
from .models import Asset, WalletAsset, UserWallet, BundleAsset, Bundle
from .api_service import request_wallet_assets

def update_wallet_asset(wallet, asset: Asset, balance: str):
    if WalletAsset.objects.filter(user_wallet=wallet, asset=asset).exists():
        walletAsset = WalletAsset.objects.get(user_wallet=wallet, asset=asset)
        walletAsset.balance = balance
        walletAsset.save()
    else:
        walletAsset = WalletAsset.objects.create(
            user_wallet=wallet,
            asset=asset,
            balance=balance
        )

@api_view(['GET'])
def get_wallet_assets(request, address: str):
    refresh = request.query_params.get('refresh', "False")
    refresh = refresh.lower() == "true"

    if not refresh:
        userAssets = WalletAsset.objects.filter(user_wallet__address=address)
        serializer = WalletAssetSerializer(userAssets, many=True)
        return Response(serializer.data)

    try:
        data = request_wallet_assets(address)
    except aiohttp.ClientError as e:
        return Response({"error": str(e)}, status=400)

    wallet, _ = UserWallet.objects.get_or_create(address=address)

    for asset in data["tokens"]:
        newAsset, _ = Asset.objects.get_or_create(
            name=asset['name'],
            symbol=asset['symbol'],
            decimals=asset['decimals'],
            address=asset['token_address'],
            total_supply=asset['total_supply'],
            asset_type=0
        )

        update_wallet_asset(wallet, newAsset, asset["balance"])

    for asset in data["nfts"]:
        newAsset, _ = Asset.objects.get_or_create(
            name=asset['name'],
            symbol=asset['symbol'],
            decimals=0,
            address=asset['token_address'],
            total_supply=asset["amount"],
            token_id=asset["token_id"],
            asset_type=1 if asset["contract_type"] == "ERC721" else 2
        )

        update_wallet_asset(wallet, newAsset, asset["amount"])

    userAssets = WalletAsset.objects.filter(user_wallet__address=address, asset__asset_type=0)
    serializer = WalletAssetSerializer(userAssets, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_bundle(request):
    try:
        data = json.loads(request.body)

        address = data["address"]
        bundle_id = data["bundle_id"]

        wallet, _ = UserWallet.objects.get_or_create(address=address)

        bundle = Bundle.objects.create(address=address, bundle_id=bundle_id)

        for model in data["bundle_assets"]:
            asset = Asset.objects.get(id=model['id'])
            BundleAsset.objects.create(bundle=bundle, asset=asset, balance=model["balance"])
        
    except KeyError as e:
        return Response({"error": f"Missing field: {str(e)}"}, status=400)

    return Response({"status": "success"})

@api_view(['GET'])
def get_wallet_bundles(request, address: str):
    bundles = Bundle.objects.filter(address=address)
    serializer = BundleSerializer(bundles, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_bundle(request, bundle_id: str):
    try:
        bundle = Bundle.objects.get(bundle_id=bundle_id)
    except Bundle.DoesNotExist:
        return Response({"error": "Bundle not found"}, status=404)

    bundle.delete()
    return Response({"status": "success"})