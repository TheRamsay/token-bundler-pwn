<script setup lang="ts" generic="TData, TValue">
import type { Column, ColumnDef, Table as TypeTable } from '@tanstack/vue-table'
import { FlexRender } from '@tanstack/vue-table'

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import type { BundleAsset } from '@/types'

defineProps<{
    table: TypeTable<BundleAsset>,
    columns: ColumnDef<BundleAsset>[],
}>()
</script>

<template>
    <div class="border rounded-md">
        <Table>
            <TableHeader>
                <TableRow v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
                    <TableHead v-for="header in headerGroup.headers" :key="header.id">
                        <FlexRender v-if="!header.isPlaceholder" :render="header.column.columnDef.header" :props="header.getContext()" />
                    </TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                <template v-if="table.getRowModel().rows?.length">
                    <TableRow v-for="row in table.getRowModel().rows" :key="row.id" :data-state="row.getIsSelected() ? 'selected' : undefined">
                        <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id">
                            <FlexRender :render="cell.column.columnDef.cell" :props="cell.getContext()" />
                        </TableCell>
                    </TableRow>
                </template>
                <template v-else>
                    <TableRow>
                        <TableCell :colSpan="columns.length" class="h-24 text-center"> No results. </TableCell>
                    </TableRow>
                </template>
            </TableBody>
        </Table>
    </div>
</template>
