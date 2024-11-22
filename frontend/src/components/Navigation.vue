<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user.store';

const items = [
  {
    url: ['/'] as string[],
    text: 'Accueil',
    connected: false,
    admin: false,
  },
  {
    url: ['/faq'] as string[],
    text: 'FAQ',
    connected: false,
    admin: false,
  },
  {
    url: [
      '/management/users',
      '/management/devices',
      '/management/whitelist',
      '/management/announces',
    ] as string[],
    text: 'Gestion',
    connected: false,
    admin: true,
  },
  {
    url: ['/helpdesk/admin'] as string[],
    text: 'Gestion des tickets',
    connected: false,
    admin: true,
  },
  /*{
    url: ['/helpdesk/user'] as string[],
    text: 'Demande d\'assistance',
    connected: true,
    admin: false,
  },*/
] as const;

const userStore = useUserStore();
const { logout } = userStore;
const { isConnected, user } = storeToRefs(userStore);

const router = useRouter();

const logout_user = async () => {
  await router.push('/');
  await logout();
};

const burger_menu = ref(false);
</script>
<template>
  <nav class="sticky top-0 z-50 h-16 border-b border-gray-300 bg-theme-nav">
    <div id="desktop" class="hidden justify-around md:flex">
      <router-link class="m-2 flex content-center items-center justify-center gap-3" to="/">
        <img alt="Logo InsaLan" class="size-[40px]" src="@/assets/images/logo_retro.png"/>
        <div class="text-xl font-bold text-white">
          Portail InsaLan
        </div>
      </router-link>
      <div class="mx-5 flex flex-1 items-center">
        <router-link
          v-for="(item, i) in items"
          :key="i"
          :to="{ path: item.url[0] }"
          :class="{
            'text-white': item.url.includes($route.path),
            'text-gray-400': !item.url.includes($route.path),
            hidden: (item.connected && !isConnected) || (item.admin && (user?.role !== 'admin' && user?.role !== 'staff')),
          }"
          class="mx-2 py-5 text-center transition duration-150 ease-in-out hover:text-white"
        >
          {{ item.text }}
        </router-link>
      </div>
      <div
        class="mx-4 my-2 flex cursor-pointer flex-col justify-center text-center font-bold text-gray-400 hover:text-white"
        :class="{ hidden: !isConnected }"
        @click="logout_user"
        @keydown.enter="logout_user"
      >
        Déconnexion
      </div>
    </div>
    <div class="md:hidden">
      <div id="top" class="flex justify-between">
        <router-link class="m-2" to="/">
          <img alt="Logo InsaLan" class="size-[40px]" src="@/assets/images/logo_retro.png"/>
        </router-link>
        <div
          class="mx-5 flex flex-1 flex-col items-center justify-center"
          :class="{ hidden: !isConnected }"
        >
          Déconnexion
        </div>
        <div class="m-2">
          <button
            class="m-auto mr-2 size-8 rounded text-center text-gray-400 ring-2 ring-gray-400 hover:text-white"
            type="button"
            @click="burger_menu = !burger_menu"
          >
            <svg
              v-if="!burger_menu"
              class="m-auto size-6 stroke-2"
              fill="none"
              stroke="currentColor"
              stroke-width="{1.5}"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <svg
              v-else
              class="m-auto size-6 stroke-2"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>
        </div>
      </div>
      <transition
        name="dropdown"
        enter-active-class="transition ease-out duration-200 transform"
        enter-from-class="-translate-y-2 opacity-0"
        enter-to-class="translate-y-0 opacity-100"
        leave-active-class="transition ease-in duration-75 transform"
        leave-from-class="translate-y-0 opacity-100"
        leave-to-class="-translate-y-2 opacity-0"
      >
        <div
          v-show="burger_menu"
          class="flex flex-col border-y border-gray-300 bg-theme-nav text-white"
        >
          <router-link
            v-for="(item, i) in items"
            :key="i"
            :to="{ path: item.url[0] }"
            :class="{
              'text-white': item.url.includes($route.path),
              'text-gray-400': !item.url.includes($route.path),
              hidden: (item.connected && !isConnected) || (item.admin && (user?.role !== 'admin' && user?.role !== 'staff')),
            }"
            class="mx-2 py-5 text-center font-bold transition duration-150 ease-in-out hover:text-blue-800"
            @click="burger_menu = !burger_menu"
          >
            {{ item.text }}
          </router-link>
        </div>
      </transition>
    </div>
  </nav>
</template>
