<script setup lang="ts">
import { storeToRefs } from 'pinia';
import PaginatedTable from '@/components/PaginatedTable.vue';
import type { Device } from '@/models/device';
import { useDeviceStore } from '@/stores/devices.store';
import { useNotificationStore } from '@/stores/notification.stores';
import { useUserStore } from '@/stores/user.store';

const { fetch_user } = useUserStore();

const userStore = useUserStore();
const { user } = storeToRefs(userStore);

const { edit_own_device, delete_own_device } = useDeviceStore();
const { addNotification } = useNotificationStore();

</script>

<template>
  <div class="m-5 flex flex-1 flex-col items-center gap-5 bg-theme-bg">
    <template
      v-if="user?.devices.length <= user?.max_device_nb"
    >
      <img
        src="@/assets/images/logo_green.png"
        alt="logo_green"
        class="pulse w-96"
      />
      <div class="text-center text-4xl">
        Bon jeu, {{ user?.username }} !
      </div>
      <div class="text-center">
        Vous êtes désormais connecté au réseau de l'InsaLan.
      </div>
    </template>
    <template
      v-else
    >
      <img
        src="@/assets/images/logo_red.png"
        alt="logo_red"
        class="w-96"
      />
      <div class="text-center text-4xl">
        Trop d'appareils connectés !
      </div>
      <div class="text-center">
        Vous avez atteint le nombre maximum d'appareils connectés au réseau.
      </div>
    </template>

    <div class="text-center">
      Vous pouvez connecter au maximum {{ user?.max_device_nb }} appareils sur le réseau.
      <br/>
      Voici la liste de vos appareils connectés au réseau :
    </div>
    <!-- Tableau des appareils connectés -->
    <div
      class="w-full lg:w-1/3"
    >
      <PaginatedTable
        :data="user?.devices as { }[]"
        :properties="[
          {
            name: 'Nom de l\'appareil',
            key: 'name',
            ordering: false,
          },
          {
            name: 'Adresse',
            key: 'mac',
            ordering: false,
          },
        ]"
        :pagination="false"
        :search="false"
        :actions="[
          {
            hint: 'Modifier l\'appareil',
            icon: 'pencil',
            key: 'update',
            modal: {
              title: 'Modifier l\'appareil',
              fields: [
                {
                  name: 'Nom',
                  key: 'name',
                  type: 'text',
                },
              ],
            },
            function: async (device, fields) => {
              if (await edit_own_device((device as unknown as Device).id, fields.name)) {
                addNotification('Appareil modifié avec succès', 'info');
                // refresh the user
                await fetch_user();
              }
            },
          },
          {
            hint: 'Supprimer l\'appareil',
            icon: 'trash-can',
            key: 'delete',
            modal: {
              title: 'Supprimer l\'appareil',
              fields: [
                {
                  name: 'Voulez-vous vraiment supprimer cet appareil ?',
                  key: 'confirm',
                  type: 'hidden',
                },
              ],
            },
            function: async (device, fields) => {
              if (await delete_own_device((device as unknown as Device).id)) {
                addNotification('Appareil supprimé avec succès', 'info');
                // refresh the user
                await fetch_user();
              }
            },
          },
        ]"
      />
    </div>
  </div>
</template>

<style>

.pulse {
  animation: pulse infinite 10s;
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
  }
}

</style>
