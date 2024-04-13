import type { Address } from "viem";
import type { Bundle, SelectedBundleAsset } from "./types";

const API_URL: string = import.meta.env.VITE_API_URL;

const sendRequest = async (url: string, method: "GET" | "POST" | "DELETE", body: any): Promise<any> => {
    const options: RequestInit = {
        method: method,
        headers: {
            "Content-Type": "application/json",
        },
    }

    if (method !== "GET") {
        options.body = JSON.stringify(body);
    }

    const data = await fetch(`${API_URL}${url}`, options);
    return await data.json();
}

export const getWalletTokens = async (walletAddress: string, refresh: boolean): Promise<Array<SelectedBundleAsset>> => {

    const json = await sendRequest(`assets/${walletAddress}?refresh=${refresh}`, "GET", {});

    return [...json].map((user_asset: any) => {
        return {
            id: user_asset.asset.id,
            symbol: user_asset.asset.symbol,
            name: user_asset.asset.name,
            balance: user_asset.balance,
            toBeBundled: "0",
            selected: false,
            address: user_asset.asset.address,
            decimals: user_asset.asset.decimals,
            displayedBalance: user_asset.balance / Math.pow(10, user_asset.asset.decimals),
            assetType: user_asset.asset.asset_type,
            tokenId: user_asset.asset.token_id,
        }
    });
}

export const createBundle = async (address: Address, bundleId: string, bundle: Array<SelectedBundleAsset>): Promise<void> => {
    const payload = {
        address: address,
        bundle_id: bundleId,
        bundle_assets: bundle.map((asset) => {
            return {
                symbol: asset.symbol,
                name: asset.name,
                balance: (BigInt(asset.toBeBundled) * BigInt(Math.pow(10, asset.decimals))).toString(),
                address: asset.address,
                decimals: asset.decimals,
                token_id: asset.tokenId,
                asset_type: asset.assetType,
                id: asset.id
            }
        })
    }

    await sendRequest("bundles", "POST", payload);
}

export const getWalletBundles = async (walletAddress: string): Promise<Array<Bundle>> => {
    const json = await sendRequest(`bundles/wallet/${walletAddress}`, "GET", {});

    return [...json].map((bundle: any) => {
        return {
            id: bundle.bundle_id,
            assets: bundle.bundle_assets.map((asset: any) => {
                return {
                    symbol: asset.asset.symbol,
                    name: asset.asset.name,
                    balance: asset.balance,
                    address: asset.asset.address,
                    decimals: asset.asset.decimals,
                    tokenId: asset.asset.token_id,
                    assetType: asset.asset.asset_type,
                    id: asset.asset.id
                }
            })
        }
    }
    )
}

export const deleteBundle = async (bundleId: string): Promise<void> => {
    await sendRequest(`bundles/${bundleId}`, "DELETE", {});
}