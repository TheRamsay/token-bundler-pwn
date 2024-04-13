from django.urls import path, register_converter
from .views import (
    get_wallet_assets,
    create_bundle,
    get_wallet_bundles,
    delete_bundle
)
from .converters import WalletAddressConverter

register_converter(WalletAddressConverter, 'address')

urlpatterns = [
    path("assets/<str:address>", get_wallet_assets),
    path("bundles", create_bundle),
    path("bundles/<str:bundle_id>", delete_bundle),
    path("bundles/wallet/<str:address>", get_wallet_bundles)
]
