<script setup lang="ts">
import type { SelectedBundleAsset } from '@/types'
import { currentBundleStore } from '../stores/store'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

function setMaxToBeBundled(asset: SelectedBundleAsset) {
    currentBundleStore.changeToBeBundled(asset.address, asset.displayedBalance.toString())
}
</script>

<template>
    <div v-if="!currentBundleStore.bundle.some((b) => b.selected)">
        <h2 class="text-md font-semibold text-blue-300">Add your assets to a bundle</h2>
    </div>
    <div v-else>
        <div v-for="asset in currentBundleStore.bundle" :key="asset.id">
            <div v-if="asset.selected" class="w-full">
                <div class="flex flex-row justify-between">
                    <span class="font-semibold m-3">{{ asset.symbol ?? 'Uknown' }} - {{ asset.address }}</span>
                    <div class="flex">
                        <Input class="w-1/2" v-model:model-value="asset.toBeBundled" />
                        <Button variant="link" class="text-blue-300" @click="() => setMaxToBeBundled(asset)">Max</Button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
