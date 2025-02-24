<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useUserStore } from '@/stores/user.store';

const { login } = useUserStore();

const LAN = (import.meta.env.VITE_LAN as string) === '1';

const login_form = reactive({
  username: '',
  password: '',
});

const login_user = async () => {
  // Change the login button to a loading spinner
  const login_button = document.getElementById('login_button');
  if (login_button) {
    login_button.classList.add('cursor-wait');
    login_button.textContent = 'Connexion en cours...';
  }

  await login(login_form.username, login_form.password);

  // Change the login button back to normal
  if (login_button) {
    login_button.classList.remove('cursor-wait');
    login_button.textContent = 'Se connecter';
  }
};

const showPassword = ref(false);
</script>

<template>
  <div class="m-4 flex flex-col items-center justify-center gap-16 md:m-16">
    <div class="flex flex-col gap-2 text-center">
      <h1 class="text-center text-2xl font-bold md:text-4xl">
        Bienvenue sur le réseau de l'InsaLan !
      </h1>
      <div>
        Pour pouvoir accéder à internet et aux serveurs de jeu, il faut vous identifier avec votre compte.
      </div>
      <div
        v-if="LAN"
        class="text-sm text-gray-500"
      >
        Votre nom
        <b
          class="text-red-500"
        >
          d'utilisateur⋅rice
        </b>
        et votre
        <b
          class="text-red-500"
        >
          mot de passe
        </b>
        sont les mêmes que sur
        <b>
          <a href="https://insalan.fr" target="_blank" rel="noopener noreferrer" class="text-blue-500">
            insalan.fr
          </a>
        </b>
      </div>
    </div>
    <form class="flex w-full flex-col gap-3 md:w-1/3">
      <div class="flex flex-col gap-2">
        <label for="username">Nom d'utilisateur⋅rice</label>
        <input id="username" v-model="login_form.username" type="text" name="username" required class="rounded-lg border border-black bg-theme-nav text-white"/>
      </div>
      <div class="flex flex-col gap-2">
        <label for="password">Mot de passe</label>
        <div class="relative">
          <input id="password" v-model="login_form.password" :type="showPassword ? 'text' : 'password'" name="password" required class="w-full flex-1 rounded-lg border border-black bg-theme-nav text-white"/>
          <button type="button" class="absolute right-3 top-2 text-white" @click.prevent="showPassword = !showPassword">
            <fa-awesome-icon v-if="showPassword" icon="eye-slash" class="size-6"/>
            <fa-awesome-icon v-else icon="eye" class="size-6"/>
          </button>
        </div>
      </div>
      <button id="login_button" type="submit" class="my-8 rounded-lg bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700" @click.prevent="login_user">
        Se connecter
      </button>
    </form>
  </div>
</template>
