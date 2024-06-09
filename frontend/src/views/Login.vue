<script setup lang="ts">
import { reactive, ref } from 'vue';
import { useUserStore } from '@/stores/user.store';

const { login } = useUserStore();

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

  const errors = await login(login_form.username, login_form.password);
  // If there are errors, display them
  if (errors) {
    const login_error = document.getElementById('login_error');
    if (login_error) {
      login_error.classList.remove('hidden');
      login_error.classList.add('block');
      login_error.textContent = errors;
    }
  }

  // Change the login button back to normal
  if (login_button) {
    login_button.classList.remove('cursor-wait');
    login_button.textContent = 'Se connecter';
  }
};

const showPassword = ref(false);
</script>

<template>
  <div class="m-4 flex flex-col items-center justify-center gap-16 lg:m-16">
    <div class="flex flex-col gap-2">
      <h1 class="text-center text-2xl font-bold lg:text-4xl">
        Bienvenue sur le réseau de l'InsaLan !
      </h1>
      <div>
        Pour pouvoir accéder à internet et aux serveurs de jeu, il faut vous identifier avec votre compte insalan.fr
      </div>
    </div>
    <form class="flex w-full flex-col gap-3 lg:w-1/3">
      <div id="login_error" class="hidden rounded-lg border border-red-500 p-4 text-red-500">
        Erreur lors de la connexion, veuillez réessayer.
      </div>
      <div class="flex flex-col gap-2">
        <label for="username">Nom d'utilisateur</label>
        <input id="username" v-model="login_form.username" type="text" name="username" required class="rounded-lg border border-black bg-theme-nav text-white"/>
      </div>
      <div class="flex flex-col gap-2">
        <label for="password">Mot de passe</label>
        <div class="relative">
          <input id="password" v-model="login_form.password" :type="showPassword ? 'text' : 'password'" name="password" required class="w-full flex-1 rounded-lg border border-black bg-theme-nav text-white"/>
          <button type="button" class="absolute right-3 top-2 text-white" @click.prevent="showPassword = !showPassword">
            <fa-awesome-icon v-if="showPassword" icon="eye-slash" class="h-6 w-6"/>
            <fa-awesome-icon v-else icon="eye" class="h-6 w-6"/>
          </button>
        </div>
      </div>
      <button id="login_button" type="submit" class="my-8 rounded-lg bg-blue-500 px-4 py-2 font-bold text-white hover:bg-blue-700" @click.prevent="login_user">
        Se connecter
      </button>
    </form>
  </div>
</template>
