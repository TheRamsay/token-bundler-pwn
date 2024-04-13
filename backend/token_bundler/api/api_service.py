from token_bundler.settings import API_KEY
import requests

API_URL = "https://deep-index.moralis.io/api/v2.2"

def fetch_data(url: str):
    headers = {
        "accept": "application/json",
        "X-API-Key": API_KEY
    }

    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()

def request_wallet_assets(address):
    url1 = f"{API_URL}/{address}/erc20?chain=sepolia"
    url2 = f"{API_URL}/{address}/nft?chain=sepolia"

    tokens_data = fetch_data(url1)
    nfts_data = fetch_data(url2) 

    return {
        "tokens": tokens_data,
        "nfts": nfts_data["result"]
    }