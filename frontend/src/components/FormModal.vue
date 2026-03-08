<script setup lang="ts">
import { ref } from 'vue';
import { useUserStore } from '@/stores/user.store';

const { create_temp_password } = useUserStore();

export interface Props {
  open: boolean;
  title: string;
  body?: string;
  buttons: 'OK' | 'ValiderAnnuler' | 'AccepterRefuser' | 'None';
  fields: {
    name: string;
    key: string;
    value: string;
    type: string;
    choices?: { key: string; value: string }[];
    required?: boolean;
  }[];
  function: () => void;
}

const props = defineProps<Props>();
defineEmits(['update:open']);

const showPassword = ref<{ [key: string]: boolean }>({});
const focusedField = ref<string | null>(null);

const unfocus = () => {
  // Source - https://stackoverflow.com/a/56899483
  // Posted by Wilco, modified by community. See post 'Timeline' for change history
  // Retrieved 2026-03-08, License - CC BY-SA 4.0

  if (document.activeElement instanceof HTMLElement) document.activeElement.blur();
};
</script>
<template>
  <div
    v-show="props.open"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    @click.self="$emit('update:open', false)"
    @keydown.escape="$emit('update:open', false)"
  >
    <form
      class="flex min-w-[20%] max-w-2xl flex-col rounded-lg bg-theme-bg p-4"
      @submit.prevent="props.function"
    >
      <div class="mb-4 flex items-center justify-between">
        <h2 class="text-2xl text-white">
          {{ props.title }}
        </h2>
        <button
          class="float-right mx-2 text-2xl text-gray-300"
          type="button"
          @click="$emit('update:open', false)"
        >
          &times;
        </button>
      </div>
      <div v-if="$slots.body" class="mb-4 text-white">
        <slot name="body"/>
      </div>
      <div v-if="props.fields.length > 0" class="mb-4 flex flex-col gap-4">
        <div
          v-for="field in props.fields"
          :key="field.key"
          class="flex flex-col"
        >
          <label :for="field.key" class="text-sm text-gray-300">{{ field.name }}</label>
          <select
            v-if="field.choices && field.type === 'text'"
            :id="field.key"
            v-model="field.value"
            class="rounded-md border border-black bg-theme-nav p-2 text-white"
            :required="field.required"
          >
            <option
              v-for="choice in field.choices"
              :key="choice.key"
              :value="choice.key"
            >
              {{ choice.value }}
            </option>
          </select>
          <div v-else-if="field.choices && field.type === 'number'" class="relative inline-block">
            <input
              :id="field.key"
              v-model="field.value"
              type="number"
              class="w-full rounded-md border border-black bg-theme-nav p-2 text-white"
              :required="field.required"
              :list="`${field.key}-choices`"
              @focus="focusedField = field.key"
              @blur="focusedField = null"
            >
            <ul
              v-show="focusedField === field.key"
              :id="`${field.key}-choices`"
              class="absolute z-20 mt-1 max-h-48 w-full overflow-y-auto rounded-md border border-black bg-theme-nav shadow-lg"
              @mousedown.prevent
            >
              <li
                v-for="choice in field.choices"
                :key="choice.key"
                class="cursor-pointer px-3 py-2 text-sm text-gray-200 hover:bg-black/30 hover:text-white"
                @click="field.value = choice.key; unfocus()"
                @keydown.enter="field.value = choice.key; unfocus()"
              >
                {{ choice.value }}
              </li>
            </ul>
          </div>
          <textarea
            v-else-if="field.type === 'textarea'"
            :id="field.key"
            v-model="field.value"
            class="h-48 rounded-md border border-black bg-theme-nav p-2 text-white"
            :required="field.required"
          />
          <div v-else-if="field.type === 'checkbox'" class="flex items-center">
            <input
              :id="field.key"
              v-model="field.value"
              type="checkbox"
              class="ml-auto rounded-md border border-black bg-theme-nav p-2 text-white"
            />
          </div>
          <div v-else-if="field.type === 'readonly'">
            <pre v-if="typeof field.value === 'boolean' && field.value === false" class="whitespace-pre-wrap">✘ Non</pre>
            <pre v-else-if="typeof field.value === 'boolean' && field.value === true" class="whitespace-pre-wrap">✔ Oui</pre>
            <pre v-else class="whitespace-pre-wrap">{{ field.value }}</pre>
          </div>
          <!-- If type is password, don't autocomplete with saved password -->
          <div
            v-else
            class="relative flex w-full items-center"
          >
            <input
              :id="field.key"
              v-model="field.value"
              :type="field.type === 'password' ? (showPassword[field.key] ? 'text' : 'password') : field.type"
              class="w-full rounded-md border border-black bg-theme-nav p-2 text-white"
              autocomplete="off"
              :required="field.required"
            />
            <!-- Button to hide / show the password -->
            <button
              v-if="field.type === 'password'"
              class="absolute right-8 top-2 text-white"
              type="button"
              @click="showPassword[field.key] = !showPassword[field.key]"
            >
              <fa-awesome-icon
                v-if="!showPassword[field.key]"
                icon="eye"
              />
              <fa-awesome-icon
                v-else
                icon="eye-slash"
              />
            </button>
            <!-- Button to regenerate a password -->
            <button
              v-if="field.type === 'password'"
              class="absolute right-2 top-2 text-white"
              type="button"
              @click="field.value = create_temp_password(); showPassword[field.key] = true"
            >
              <fa-awesome-icon
                icon="redo"
              />
            </button>
          </div>
        </div>
      </div>
      <div
        v-if="props.buttons === 'ValiderAnnuler'"
        class="flex justify-end"
      >
        <button
          class="mr-2 rounded-md bg-theme-nav px-4 py-2 text-white"
          type="button"
          @click="$emit('update:open', false)"
        >
          Annuler
        </button>
        <button
          class="rounded-md bg-blue-700 px-4 py-2 text-white"
          type="submit"
        >
          Valider
        </button>
      </div>
      <div
        v-if="props.buttons === 'AccepterRefuser'"
        class="flex justify-end"
      >
        <button
          class="mr-2 rounded-md bg-theme-nav px-4 py-2 text-white"
          type="button"
          @click="$emit('update:open', false)"
        >
          Refuser
        </button>
        <button
          class="rounded-md bg-blue-700 px-4 py-2 text-white"
          type="submit"
        >
          Accepter
        </button>
      </div>
      <div
        v-else-if="props.buttons === 'OK'"
        class="flex justify-end"
      >
        <button
          class="mr-2 rounded-md bg-blue-700 px-4 py-2 text-white"
          type="button"
          @click="$emit('update:open', false)"
        >
          Ok
        </button>
      </div>
    </form>
  </div>
</template>
