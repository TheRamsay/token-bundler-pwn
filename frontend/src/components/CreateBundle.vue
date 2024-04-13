<script setup lang="ts">
import { createBundle, getWalletBundles, getWalletTokens } from '@/api'
import { Button } from '@/components/ui/button'
import DataTable from '@/components/AssetsTable/DataTable.vue'
import { columns } from '@/components/AssetsTable/columns'
import { currentBundleStore, addressStore, userBundlesStore } from '@/stores/store'
import BundleList from '@/components/BundleList.vue'
import { saveBundle } from '@/blockchainClient'
import { useToast } from '@/components/ui/toast/use-toast'
import { notifyError, notifySuccess } from '@/notifications'
import { ref } from 'vue'
import { getCoreRowModel, useVueTable } from '@tanstack/vue-table'

const init = ref(false)

async function handleBundleSave() {
    const selectedAssets = currentBundleStore.bundle.filter((x) => x.selected)

    if (selectedAssets.length == 0) {
        return
    }

    if (!addressStore.address) {
        return
    }

    for (const asset of selectedAssets) {
        const numberToBeBundled = Number(asset.toBeBundled)
        console.log(numberToBeBundled)

        if (isNaN(numberToBeBundled)) {
            notifyError('Input error', 'You must enter a number')
            return
        }

        if (numberToBeBundled > asset.displayedBalance) {
            notifyError('Input error', 'You cannot bundle more than you have')
            return
        }

        if (numberToBeBundled <= 0) {
            notifyError('Input error', 'You have to bundle an positive amount')
            return
        }
    }
    try {
        const bundleId = await saveBundle(selectedAssets)
        currentBundleStore.load(await getWalletTokens(addressStore.address, true))
        await createBundle(addressStore.address, bundleId, selectedAssets)
        userBundlesStore.load(await getWalletBundles(addressStore.address))
        notifySuccess('Your bundle has been created successfully')
    } catch (error) {
        notifyError('Error', 'An error occurred while bundling assets')
        console.error(error)
    } finally {
        table.resetRowSelection()
    }
}

const table = useVueTable({
    get data() {
        return currentBundleStore.bundle
    },
    get columns() {
        return columns
    },
    getCoreRowModel: getCoreRowModel()
})
</script>

<template>
    <div>
        <div class="flex justify-between mb-4 items-center">
            <h2 class="text-xl font-semibold mb-4">Your assets</h2>
            <Button
                class="bg-blue-300 hover:bg-blue-600 text-gray-950"
                @click="() => getWalletTokens(addressStore.address!, true).then((x) => currentBundleStore.load(x))"
                >Refresh</Button
            >
        </div>
        <DataTable :table="table" :columns="columns" :init="init" />
    </div>
    <div>
        <h2 class="text-xl font-semibold my-4">Your bundle</h2>
        <BundleList />
        <Button class="my-4 bg-blue-300 hover:bg-blue-600 text-gray-950" @click="() => handleBundleSave()">Bundle</Button>
    </div>
</template>
