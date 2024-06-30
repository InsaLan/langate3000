<script setup lang="ts">
import { defineProps } from 'vue';

export interface Props {
  type: string;
}

const props = defineProps<Props>();
</script>

<template>
  <div class="flex flex-col md:w-1/6">
    <router-link
      to="/management/users"
      class="rounded-lg p-2 text-blue-500"
      :class="{ 'bg-gray-600 text-white': props.type === 'users' }"
    >
      Utilisateurs
    </router-link>
    <router-link
      to="/management/devices"
      class="rounded-lg p-2 text-blue-500"
      :class="{ 'bg-gray-600 text-white': props.type === 'devices' }"
    >
      Appareils
    </router-link>
    <router-link
      to="/management/whitelist"
      class="rounded-lg p-2 text-blue-500"
      :class="{ 'bg-gray-600 text-white': props.type === 'whitelist' }"
    >
      Appareils en whitelist
    </router-link>
    <router-link
      to="/management/announces"
      class="rounded-lg p-2 text-blue-500"
      :class="{ 'bg-gray-600 text-white': props.type === 'announces' }"
    >
      Annonces
    </router-link>
  </div>
</template>
