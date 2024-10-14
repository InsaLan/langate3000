<script setup lang="ts">

let nb = 1;

const shakeLogo = () => {
  const logo = document.querySelector('#logo');
  if (logo && logo.classList && logo.classList.contains('shake') === false && logo.classList.contains('move') === false) {
    if (nb % 10 === 0) {
      logo.classList.add('move');
      setTimeout(() => {
        logo.classList.remove('move');
        nb += 1;
      }, 3000);
    } else {
      logo.classList.add('shake');
      setTimeout(() => {
        logo.classList.remove('shake');
        nb += 1;
      }, 1000);
    }
  }
};

</script>
<template>
  <div class="flex flex-1 flex-col items-center justify-center text-white">
    <div class="flex flex-col items-center justify-center gap-5 rounded-xl border-2 border-white p-5">
      <div class="text-8xl font-bold before:mb-5 before:text-8xl before:font-bold before:content-['-'] after:mt-5 after:text-8xl after:font-bold after:content-['-']">
        404
      </div>
      <div class="flex w-full items-center justify-center border-y-2 border-white p-2">
        <img
          id="logo"
          alt="Logo InsaLan"
          class="size-[100px]"
          src="@/assets/images/logo_retro.png"
          @click="shakeLogo"
          @keydown.enter="shakeLogo"
        />
      </div>
      <div class="text-4xl font-bold">
        Page non trouvée
      </div>
      <div class="text-center text-2xl">
        La page que vous cherchez n'existe pas.
        <br/>
        Veuillez vérifier l'URL ou revenir à
        <router-link to="/" class="text-blue-400 hover:text-blue-300">
          l'accueil
        </router-link>
      </div>
    </div>
  </div>
</template>

<style>

.shake {
  animation: shake 0.5s;
}

@keyframes shake {
  0% { transform: translate(1px, 1px) rotate(0deg); }
  10% { transform: translate(-1px, -2px) rotate(-1deg); }
  20% { transform: translate(-3px, 0px) rotate(1deg); }
  30% { transform: translate(3px, 2px) rotate(0deg); }
  40% { transform: translate(1px, -1px) rotate(1deg); }
  50% { transform: translate(-1px, 2px) rotate(-1deg); }
  60% { transform: translate(-3px, 1px) rotate(0deg); }
  70% { transform: translate(3px, 1px) rotate(-1deg); }
  80% { transform: translate(-1px, -1px) rotate(1deg); }
  90% { transform: translate(1px, 2px) rotate(0deg); }
  100% { transform: translate(1px, -2px) rotate(-1deg); }
}

.move {
  animation: move 3s;
}

@keyframes move {
  0% { transform: translate(0, 0) rotate(0deg); }
  20% { transform: translate(170px, 0) rotate(90deg); }
  40% { transform: translate(0, 0) rotate(0deg); }
  60% { transform: translate(-170px, 0) rotate(-90deg); }
  80% { transform: translate(0, 0) rotate(0deg); }
  100% { transform: translate(0, 0) rotate(360deg); }
}

</style>
