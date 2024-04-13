import type { BundleAsset } from '@/types'
import type { ColumnDef } from '@tanstack/vue-table'
import { h } from 'vue'
import Checkbox from '../ui/checkbox/Checkbox.vue'
import { currentBundleStore } from '@/stores/store'

export const columns: ColumnDef<BundleAsset>[] = [
    {
        id: 'select',
        header: ({ table }) => h(Checkbox, {
            'checked': table.getIsAllPageRowsSelected() || (table.getIsSomePageRowsSelected() && 'indeterminate'),
            'onUpdate:checked': value => {
                table.toggleAllPageRowsSelected(!!value);
                currentBundleStore.setSelectAll(!!value);
            },
            'ariaLabel': 'Select all',
        }),
        cell: ({ row }) => h(Checkbox, {
            'checked': row.getIsSelected(),
            'onUpdate:checked': value => {
                row.toggleSelected(!!value);
                currentBundleStore.flipSelected(row.getValue('address'));
            },
            'ariaLabel': 'Select row',
        }),
        enableSorting: false,
        enableHiding: false,
    },
    {
        accessorKey: "address",
        header: () => h('div', 'Address'),
    },
    {
        accessorKey: 'symbol',
        header: () => h('div', 'Symbol'),
    },
    {
        accessorKey: 'name',
        header: () => h('div', 'Name'),
    },
    {
        accessorKey: 'displayedBalance',
        header: () => h('div', { class: 'text-right' }, 'Balance'),
        cell: ({ row }) => {
            const amount = row.getValue<number>('displayedBalance');
            return h('div', { class: 'text-right font-medium' }, amount)
        },
    },
]