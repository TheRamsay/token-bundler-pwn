import type { Bundle, SelectedBundleAsset } from "@/types.ts";
import type { Address } from "viem";
import { reactive } from "vue";

export const currentBundleStore = reactive({
    bundle: [] as SelectedBundleAsset[],
    flipSelected(address: string) {
        const asset = this.bundle.find(asset => asset.address === address);

        if (asset) {
            asset.selected = !asset.selected;
        }
    },
    changeToBeBundled(address: string, value: number) {
        const asset = this.bundle.find(asset => asset.address == address);

        if (asset) {
            asset.toBeBundled = value;
        }
    },
    load(bundle: SelectedBundleAsset[]) {
        this.bundle = bundle;
    },
    setSelectAll(value: boolean) {
        this.bundle.forEach(asset => asset.selected = value);
    },
});

export const addressStore = reactive({
    address: undefined as Address | undefined,
    setAddress(address: Address) {
        this.address = address;
    },
    clearAddress() {
        this.address = undefined;
    }
});

export const userBundlesStore = reactive({
    bundles: [] as Bundle[],
    load(bundles: Bundle[]) {
        this.bundles = bundles;
    }
});