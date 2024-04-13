<script setup lang="ts">
import YourBundles from '@/components/YourBundles.vue'
import CreateBundle from '@/components/CreateBundle.vue'
import Navbar from '@/components/Navbar.vue'
import { ref, computed } from 'vue'
import { addressStore } from '@/stores/store'
import Toaster from '@/components/ui/toast/Toaster.vue'

const routes = {
    '/': YourBundles,
    '/create': CreateBundle
}

const currentPath = ref(window.location.hash)

window.addEventListener('hashchange', () => {
    currentPath.value = window.location.hash
})

const currentView = computed(() => {
    return routes[currentPath.value.slice(1) || '/']
})
</script>

<template>
    <div>
        <Navbar />
        <div v-if="addressStore.address">
            <component :is="currentView" />
        </div>
        <div v-else>
            <h2 class="text-xl font-bold text-blue-300">Please connect your wallet to continue</h2>
        </div>
        <Toaster />
    </div>
</template>
