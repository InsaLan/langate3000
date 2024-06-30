<script setup lang="ts">
import ManagementMenu from '@/components/ManagementMenu.vue';

</script>

<template>
  <div class="m-4 flex flex-col">
    <div class="mb-5 border-b-2 border-gray-500 pb-2 text-4xl font-bold text-gray-300">
      Interface d'administration
    </div>
    <div class="flex flex-col md:flex-row">
      <ManagementMenu type="announces"/>
    </div>
  </div>
</template>
