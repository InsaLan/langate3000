<script setup lang="ts">
import MarkdownIt from 'markdown-it';
import { ref } from 'vue';

const FAQ = {
  Compte: [
    {
      question: "J'ai perdu mon mot de passe",
      answer: 'Un membre du staff peut le réinitialiser pour vous.',
      visible: ref(false),
    },
    {
      question: "Je n'arrive pas à me connecter",
      answer: 'Vérifiez vos identifiants, et n\'hésitez pas à demander de l\'aide à un membre du staff qui vous aidera.',
      visible: ref(false),
    },
  ],
  Réseau: [
    {
      question: 'Mon ordinateur ne se connecte pas au réseau ou indique que la connexion est limitée',
      answer: '- Revérifiez que votre câble réseau est bien branché.\n- Vérifiez que le cable connectant votre switch au reste du réseau n\'a pas été débranché (il doit être sur le dernier port du switch).\n- Vérifiez que vous n\'utilisez pas de VPN.\n- Vérifiez que le pilote de votre carte réseau est bien installé.\n- Vérifiez que vous n\'avez pas configuré une adresse IP statique.\n- Si votre problème n\'est pas résolu, n\'hésitez pas à contacter un membre du staff qui vous aidera.',
      visible: ref(false),
    },
    {
      question: 'J\'ai accès à certains sites/jeux mais pas à d\'autres',
      answer: 'Si vous pensez que vous devriez y avoir accès, vous pouvez contacter un membre du staff.',
      visible: ref(false),
    },
  ],
};

const md = new MarkdownIt(
  {
    html: true,
    linkify: true,
  },
);

md.renderer.rules.link_open = function customLinkOpen(tokens, idx, options, env, self) {
  tokens[idx].attrPush(['class', 'text-blue-500']);
  tokens[idx].attrPush(['target', '_blank']);
  tokens[idx].attrPush(['rel', 'noopener noreferrer']);
  return self.renderToken(tokens, idx, options);
};

md.renderer.rules.list_item_open = function listItemOpen(tokens, idx, options, env, self) {
  tokens[idx].attrPush(['class', 'list-disc ml-5']);
  return self.renderToken(tokens, idx, options);
};

</script>

<template>
  <div class="m-5 flex flex-1 flex-col items-center gap-5 bg-theme-bg">
    <div class="text-center text-4xl">
      Foire aux Questions
    </div>
    <div class="text-center">
      Cette page regroupe les questions régulièrement posées au sujet du réseau de
      l'InsaLan et du fonctionnement de ce portail captif.
    </div>
    <div id="questions" class="flex flex-col gap-5 md:w-3/5">
      <div v-for="(questions, categorie) in FAQ" :key="categorie" class="flex flex-col gap-5">
        <div class="border-b-2 border-gray-600 text-2xl text-gray-300">
          {{ categorie }}
        </div>
        <div class="flex flex-col gap-2">
          <div v-for="(question, i) in questions" :key="i" class="flex flex-col gap-2">
            <div
              class="cursor-pointer text-blue-500"
              @click="question.visible.value = !question.visible.value"
              @keydown.enter="question.visible.value = !question.visible.value"
            >
              {{ question.question }}
              <fa-awesome-icon
                v-if="question.visible.value"
                icon="chevron-up"
                class="size-3"
              />
              <fa-awesome-icon
                v-else
                icon="chevron-down"
                class="size-3"
              />
            </div>
            <transition
              name="dropdown"
              enter-active-class="transition ease-out duration-200 transform"
              enter-from-class="opacity-0"
              enter-to-class="opacity-100"
              leave-active-class="transition ease-in duration-200 transform"
              leave-from-class="opacity-100"
              leave-to-class="opacity-0"
            >
              <!-- This content is markdown and not a user input, so we can trust it -->
              <!-- eslint-disable -->
              <div
                v-if="question.visible.value"
                class="mx-5 text-white transition-opacity duration-500"
                v-html="md.render(question.answer)"
              />
            </transition>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
