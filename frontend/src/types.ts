import type { Address } from "viem"

export type BundleAsset = {
    id: number,
    assetType: AssetType,
    symbol: string | null
    name: string | null
    balance: number
    address: Address,
    decimals: number,
    tokenId: string,
}

export type SelectedBundleAsset = BundleAsset & {
    toBeBundled: string 
    selected: boolean
    displayedBalance: number,
}

export type Bundle = {
    id: string
    assets: BundleAsset[]
}

export enum AssetType {
    ERC20 = 0,
    ERC721 = 1,
    ERC1155 = 2
}