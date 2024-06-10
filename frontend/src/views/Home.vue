<script setup lang="ts">
import { useUserStore } from '@/stores/user.store';

const userStore = useUserStore();
const { user } = userStore;

</script>

<template>
  <div class="m-5 flex flex-1 flex-col items-center gap-5 bg-theme-bg">
    <img src="@/assets/images/logo_green.png" alt="logo_green" class="pulse w-96"/>
    <div class="text-center text-4xl">
      Bon jeu, {{ user?.username }} !
    </div>
    <div class="text-center">
      Vous êtes désormais connecté au réseau de l'InsaLan.
    </div>
    <div class="text-center">
      Vous pouvez connecter au maximum {{ user?.max_device_nb }} appareils sur le réseau.
      <br/>
      Voici la liste de vos appareils connectés au réseau :
    </div>
    <!-- Tableau des appareils connectés -->
    <table class="table-auto border-collapse border border-gray-800 bg-theme-nav text-gray-400 lg:w-1/3">
      <thead>
        <tr>
          <th class="border border-gray-800">
            #
          </th>
          <th class="border border-gray-800">
            Nom de l'appareil
          </th>
          <th class="border border-gray-800">
            Réseau
          </th>
          <th class="border border-gray-800">
            Actions
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(device, i) in user?.devices" :key="i">
          <td class="border border-gray-800 p-1 px-2">
            {{ i }}
          </td>
          <td class="border border-gray-800 p-1 px-2">
            {{ device.name }}
          </td>
          <td class="border border-gray-800 p-1 px-2">
            {{ device.area }}
          </td>
          <td class="w-1/6 border border-gray-800 p-1 px-2">
            <div class="flex items-center justify-center gap-2">
              <div class="group relative h-8 w-8 cursor-pointer rounded bg-gray-500 p-1 text-center hover:bg-gray-600">
                <fa-awesome-icon icon="pencil" class="text-white"/>
                <div class="pointer-events-none absolute left-0 top-0 z-20 mr-10 mt-10 w-32 rounded bg-gray-800 p-2 text-xs text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100">
                  Modifier l'appareil
                </div>
              </div>
              <div class="group relative h-8 w-8 cursor-pointer rounded bg-gray-500 p-1 text-center hover:bg-gray-600">
                <fa-awesome-icon icon="trash-can" class="text-white"/>
                <div class="pointer-events-none absolute left-0 top-0 z-20 mr-10 mt-10 w-32 rounded bg-gray-800 p-2 text-xs text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100">
                  Supprimer l'appareil
                </div>
              </div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
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
