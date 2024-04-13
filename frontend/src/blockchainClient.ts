import { http, createConfig } from 'use-wagmi'
import { mainnet, sepolia } from 'use-wagmi/chains'
import { injected } from 'use-wagmi/connectors'
import { createPublicClient, createWalletClient, custom, erc20Abi, getContract, type Address } from 'viem'
import { contractAbi } from './abi'
import type { SelectedBundleAsset } from './types'
import { addressStore } from './stores/store'

export const config = createConfig({
    chains: [sepolia],
    connectors: [
        injected()
    ],
    transports: {
        [mainnet.id]: http(),
        [sepolia.id]: http(),
    },
})

export const contractAddress = import.meta.env.VITE_CONTRACT_ADDRESS as Address

export const publicClient = createPublicClient({
    chain: sepolia,
    transport: http()
})

export const walletClient = createWalletClient({
    account: '0x0bBA9E6297b471339F15eD17AA6aFc320226A264',
    chain: sepolia,
    transport: custom(window.ethereum)
})

export const approveToken = async (asset: SelectedBundleAsset) => {
    const tokenContract = getContract({
        address: asset.address,
        abi: erc20Abi,
        client: {
            public: publicClient,
            wallet: walletClient
        }
    })

    const hash = await tokenContract.write.approve([contractAddress, BigInt(asset.toBeBundled) * BigInt(Math.pow(10, asset.decimals))])
    await publicClient.waitForTransactionReceipt({
        hash
    })
}

export const saveBundle = async (selectedAssets: SelectedBundleAsset[]): Promise<string> => {
    // Approve all selected assets
    await Promise.all(selectedAssets.map((asset) => approveToken(asset)))

    const bundleContract = getContract({
        address: contractAddress,
        abi: contractAbi,
        client: {
            public: publicClient,
            wallet: walletClient
        }
    })

    const data = selectedAssets.map((asset) => {
        return [asset.assetType, asset.address, BigInt(asset.tokenId), BigInt(asset.toBeBundled) * BigInt(Math.pow(10, asset.decimals))]
    })

    // Retrieve the bundle id
    const { result } = await publicClient.simulateContract({
        address: contractAddress,
        abi: contractAbi,
        functionName: 'create',
        args: [data],
        account: addressStore.address
    })

    const bundleId = (result as bigint).toString()

    const hash = await bundleContract.write.create([data])
    await publicClient.waitForTransactionReceipt({
        hash
    })

    return bundleId;
}

export const unwrapBundle = async (bundleId: string) => {
    const { request } = await publicClient.simulateContract({
        address: contractAddress,
        abi: contractAbi,
        functionName: 'unwrap',
        args: [BigInt(bundleId)],
        account: addressStore.address
    })

    const hash = await walletClient.writeContract(request)

    await publicClient.waitForTransactionReceipt({
        hash
    })
}

export const connectWallet = async (): Promise<Address> => {
    const [address] = await walletClient.requestAddresses()
    return address
}