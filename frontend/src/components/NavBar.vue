<script setup lang="ts">
import { addressStore, currentBundleStore, userBundlesStore } from '../stores/store'
import { getWalletTokens } from '@/api'
import { Button } from '@/components/ui/button'
import { getWalletBundles } from '@/api'
import { onMounted } from 'vue'
import { connectWallet } from '@/blockchainClient'
import type { Address } from 'viem'
import { notifyError } from '@/notifications'

async function prepareData(address: Address) {
    try {
        addressStore.setAddress(address)
        currentBundleStore.load(await getWalletTokens(address, true))
        userBundlesStore.load(await getWalletBundles(address))
    } catch (error) {
        notifyError('Error', 'An error occurred while fetching data')
        console.error(error)
    }
}

async function walletConnect() {
    const address = await connectWallet()
    localStorage.setItem('address', address)
    await prepareData(address)
}

onMounted(async () => {
    const address = localStorage.getItem('address') as Address | null
    if (address) {
        await prepareData(address)
    }
})
</script>
<template>
    <div class="my-8 flex flex-row justify-between w-full items-end">
        <h1 class="text-2xl font-bold mr-8">Token bundler</h1>
        <div class="flex gap-4 sm:gap-6 mr-auto">
            <a class="font-medium text-md hover:underline underline-offset-4 text-teal-400" href="#/">Bundles</a>
            <a class="font-medium text-md hover:underline underline-offset-4 text-teal-400" href="#/create">Create bundle</a>
        </div>
        <div v-if="addressStore.address" class="flex justify-between w-1/2 items-center">
            <div>
                Address: <span class="text-teal-400 font-semibold">{{ addressStore.address }} </span>
            </div>
            <Button class="bg-blue-300 hover:bg-blue-600 text-gray-950" @click="() => addressStore.clearAddress()">Disconnect</Button>
        </div>
        <div v-else>
            <Button class="bg-blue-300 hover:bg-blue-600 text-gray-950" @click="walletConnect">Connect wallet</Button>
        </div>
    </div>
</template>
