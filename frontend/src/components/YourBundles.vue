<script setup lang="ts">
import { addressStore, currentBundleStore, userBundlesStore } from '@/stores/store'
import { ChevronsUpDown } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { unwrapBundle } from '@/blockchainClient'
import { deleteBundle, getWalletBundles, getWalletTokens } from '@/api'
import { notifyError, notifySuccess } from '@/notifications'

async function handleUnwrapBundle(bundleId: string) {
    try {
        await unwrapBundle(bundleId)
        await deleteBundle(bundleId)
        if (addressStore.address) {
            userBundlesStore.load(await getWalletBundles(addressStore.address))
            currentBundleStore.load(await getWalletTokens(addressStore.address, true))
        }
    } catch (error) {
        notifyError('Error', 'An error occurred while unwrapping bundle')
        console.error(error)
        return
    }

    notifySuccess('Your bundle has been unwrapped successfully')
}
</script>

<template>
    <div>
        <h2 class="text-xl font-semibold mb-2">Your bundles</h2>
        <div v-if="userBundlesStore.bundles.length === 0">
            <p>No bundles found</p>
        </div>
        <div v-else>
            <div v-for="bundle in userBundlesStore.bundles" :key="bundle.id">
                <div class="my-4">
                    <Collapsible class="w-[350px] space-y-2">
                        <div class="flex items-center justify-between space-x-4 px-4">
                            <div class="flex items-center">
                                <h4 class="text-sm font-semibold">Bundle {{ bundle.id }} has {{ bundle.assets.length }} assets</h4>
                                <Button @click="() => handleUnwrapBundle(bundle.id)" variant="link" class="text-red-300">Unwrap</Button>
                            </div>
                            <CollapsibleTrigger as-child>
                                <Button variant="ghost" size="sm" class="w-9 p-0">
                                    <ChevronsUpDown class="h-4 w-4" />
                                    <span class="sr-only">Toggle</span>
                                </Button>
                            </CollapsibleTrigger>
                        </div>
                        <CollapsibleContent class="space-y-2 ml-4">
                            <div v-for="asset in bundle.assets" :key="asset.address" class="flex items">
                                <div class="rounded-md border px-4 py-3 font-mono text-sm cursor-pointer">
                                    {{ asset.symbol }} - {{ asset.balance / Math.pow(10, asset.decimals) }}
                                </div>
                            </div>
                        </CollapsibleContent>
                    </Collapsible>
                </div>
            </div>
        </div>
    </div>
</template>
