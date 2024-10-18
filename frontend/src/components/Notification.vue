<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { useNotificationStore } from '@/stores/notification.stores';

const notificationStore = useNotificationStore();
const { notifications } = storeToRefs(notificationStore);
</script>

<template>
  <div class="fixed bottom-4 right-4 z-50 space-y-2">
    <TransitionGroup name="notification">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        :class="[
          'max-w-sm rounded-lg p-4 shadow-lg',
          'transition-all duration-300 ease-in-out',
          notification.type === 'error' ? 'bg-red-500 text-white' : 'bg-green-500 text-white',
        ]"
      >
        {{ notification.message }}
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}
.notification-enter-from,
.notification-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
