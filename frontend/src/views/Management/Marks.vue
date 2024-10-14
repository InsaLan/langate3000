<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { onMounted, ref } from 'vue';
import ManagementMenu from '@/components/ManagementMenu.vue';
import type { EditableMark, GameMark, Mark } from '@/models/mark';
import { useDeviceStore } from '@/stores/devices.store';
import { useNotificationStore } from '@/stores/notification.stores';

const { addNotification } = useNotificationStore();

const deviceStore = useDeviceStore();

const {
  fetch_marks, patch_marks, move_marks, fetch_game_marks, change_game_marks,
} = deviceStore;
const { marks, gameMarks } = storeToRefs(deviceStore);

const marksCopy = ref<EditableMark[]>([]);

const edit = ref(false);

onMounted(async () => {
  await fetch_marks();
  await fetch_game_marks();
  // make a copy of the marks
  marksCopy.value = marks.value.map((mark) => ({ ...mark }));
});

const addMark = () => {
  marksCopy.value.push({ name: '', value: 0, priority: 0 });
};

const removeMark = (index: number) => {
  marksCopy.value.splice(index, 1);
};

const submitData = async () => {
  if (await patch_marks(marksCopy.value)) {
    addNotification('Les marks ont bien été modifiées', 'info');

    edit.value = false;
    await fetch_marks();
    // make a copy of the marks
    marksCopy.value = marks.value.map((mark) => ({ ...mark }));
  }
};

const reset = async () => {
  marksCopy.value = marks.value.map((mark) => ({ ...mark }));
  edit.value = false;
};

// -- Move Modal --

const move = ref(false);
const currentMark = ref(0);
const chosenMark = ref(0);

const openModal = (selectedMark: number) => {
  currentMark.value = selectedMark;
  // set the chosen mark to the first mark in the list
  chosenMark.value = marks.value[0].value;
  move.value = true;
};

const validateMove = async () => {
  if (await move_marks(currentMark.value, chosenMark.value)) {
    addNotification('Les appareils ont bien été déplacés', 'info');
    // close the modal
    move.value = false;

    // reload the marks to update the number of devices
    await fetch_marks();
  }
};

// -- Game Edit Modal --

const game = ref(false);
const gameMarksFields = ref<string[]>([]);
const gameMarksValues = ref<string[]>([]);

const openGameModal = () => {
  // make a copy of the game marks
  gameMarksFields.value = Object.keys(gameMarks.value);
  // make a copy of the game marks values. Convert each number[] into string "value1,value2,..."
  gameMarksValues.value = Object.values(gameMarks.value).map((values) => values.join(','));

  game.value = true;
};

const submitGame = async () => {
  let valid = true;
  // if the values field are not "number,number,..."
  gameMarksValues.value.forEach((value) => {
    value.split(',').forEach((number) => {
      if (Number.isNaN(Number(number))) {
        addNotification('Les valeurs doivent être des nombres séparés par des virgules', 'error');
        valid = false;
      }
    });
  });

  if (!valid) {
    return;
  }

  // create a new GameMark object
  const gameMarksObject: GameMark = {};
  gameMarksFields.value.forEach((field, index) => {
    gameMarksObject[field] = gameMarksValues.value[index].split(',').map((value) => Number(value));
  });

  if (await change_game_marks(gameMarksObject)) {
    // close the modal
    game.value = false;

    addNotification('La répartition par jeu a bien été modifiée', 'info');

    // reload the game marks to update the number of devices
    await fetch_game_marks();
  }
};

</script>

<template>
  <div class="m-4 flex flex-col">
    <div class="mb-5 border-b-2 border-gray-500 pb-2 text-4xl font-bold text-gray-300">
      Interface d'administration
    </div>
    <div class="flex flex-col md:flex-row">
      <ManagementMenu type="marks"/>
      <div class="m-4 flex flex-1 flex-col">
        <div class="flex flex-row justify-between overflow-x-auto overflow-y-hidden md:overflow-x-hidden">
          <table class="w-full rounded-lg border border-black bg-table text-gray-300">
            <thead
              class="bg-zinc-800"
            >
              <tr>
                <th class="border-2 border-zinc-800 px-2">
                  Name
                </th>
                <th class="border-2 border-zinc-800 px-2">
                  Value
                </th>
                <th class="border-2 border-zinc-800 px-2">
                  Priority
                </th>
                <th
                  v-if="!edit"
                  class="border-2 border-zinc-800 px-2"
                >
                  Nb Appareils
                </th>
                <th
                  v-if="!edit"
                  class="border-2 border-zinc-800 px-2"
                >
                  Nb Appareils (Whitelisted)
                </th>
                <th class="border-2 border-zinc-800 px-2"/>
              </tr>
            </thead>
            <tbody
              class="text-black"
            >
              <tr
                v-for="(mark, index) in edit ? marksCopy : marks"
                :key="index"
                class="border-b text-white"
              >
                <td class="border-2 border-zinc-800 p-2">
                  <template v-if="edit">
                    <label class="sr-only" for="name">Name</label>
                    <input
                      id="name"
                      v-model="mark.name"
                      class="w-full rounded-md border border-black bg-theme-nav p-2"
                      type="text"
                    />
                  </template>
                  <template v-else>
                    <strong>{{ mark.name }}</strong>
                  </template>
                </td>
                <td class="border-2 border-zinc-800 p-2">
                  <template v-if="edit">
                    <label class="sr-only" for="value">Value</label>
                    <input
                      id="value"
                      v-model.number="mark.value"
                      class="w-full rounded-md border border-black bg-theme-nav p-2"
                      type="number"
                    />
                  </template>
                  <template v-else>
                    {{ mark.value }}
                  </template>
                </td>
                <td class="border-2 border-zinc-800 p-2">
                  <template v-if="edit">
                    <div
                      class="flex flex-row gap-4"
                    >
                      <label class="sr-only" for="priority">Priority</label>
                      <!-- Add a slider alongside the input -->
                      <input
                        v-model.number="mark.priority"
                        class="w-full rounded-md border border-black bg-theme-nav p-2"
                        type="range"
                        min="0"
                        max="10"
                        step="0.1"
                      />
                      <input
                        v-model.number="mark.priority"
                        class="w-20 rounded-md border border-black bg-theme-nav p-2"
                        type="number"
                        step="0.1"
                      />
                    </div>
                  </template>
                  <template v-else>
                    {{ mark.priority }}
                  </template>
                </td>
                <td
                  v-if="!edit"
                  class="border-2 border-zinc-800 p-2 text-center"
                >
                  <div>
                    {{ (mark as Mark).devices }}
                  </div>
                </td>
                <td
                  v-if="!edit"
                  class="border-2 border-zinc-800 p-2 text-center"
                >
                  <div>
                    {{ (mark as Mark).whitelisted }}
                  </div>
                </td>
                <td class="relative border-2 border-zinc-800 p-2 text-center">
                  <template v-if="edit">
                    <button
                      class="group rounded bg-red-500 p-1 hover:bg-red-600"
                      type="button"
                      @click="removeMark(index)"
                    >
                      <fa-awesome-icon
                        icon="trash-can"
                        size="lg"
                      />
                      <div
                        class="pointer-events-none absolute right-[-40px] z-20 mr-10 mt-10 w-32 rounded bg-gray-800 p-2 text-xs text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100"
                        :class="{
                          'bottom-8': index === (edit ? marksCopy.length - 1 : marks.length - 1),
                          'top-0': index !== (edit ? marksCopy.length - 1 : marks.length - 1),
                        }"
                      >
                        Supprimer cette mark
                      </div>
                    </button>
                  </template>
                  <template v-else>
                    <div
                      class="flex justify-center gap-2"
                    >
                      <router-link
                        class="group rounded bg-blue-500 p-1 hover:bg-blue-600"
                        :to="`/management/devices?mark=${mark.value}`"
                      >
                        <fa-awesome-icon
                          icon="eye"
                          size="lg"
                        />
                        <div
                          class="pointer-events-none absolute right-[-40px] z-20 mr-10 mt-10 w-32 rounded bg-gray-800 p-2 text-xs text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100"
                          :class="{
                            'bottom-8': index === (edit ? marksCopy.length - 1 : marks.length - 1),
                            'top-0': index !== (edit ? marksCopy.length - 1 : marks.length - 1),
                          }"
                        >
                          Voir les appareils avec cette mark
                        </div>
                      </router-link>
                      <button
                        class="group rounded bg-blue-500 p-1 hover:bg-blue-600"
                        type="button"
                        @click="openModal(mark.value)"
                      >
                        <fa-awesome-icon
                          icon="arrows-alt"
                          size="lg"
                        />
                        <div
                          class="pointer-events-none absolute right-[-40px] z-20 mr-10 mt-10 w-32 rounded bg-gray-800 p-2 text-xs text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100"
                          :class="{
                            'bottom-8': index === (edit ? marksCopy.length - 1 : marks.length - 1),
                            'top-0': index !== (edit ? marksCopy.length - 1 : marks.length - 1),
                          }"
                        >
                          Déplacer les appareils avec cette mark
                        </div>
                      </button>
                    </div>
                  </template>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="mt-4 flex flex-col justify-between gap-4 md:flex-row">
          <template v-if="edit">
            <div class="flex flex-col gap-4 md:flex-row">
              <button
                class="rounded bg-red-500 px-4 py-2 text-white hover:bg-red-600"
                type="button"
                @click="reset"
              >
                Annuler
              </button>
              <button
                class="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
                type="button"
                @click="addMark"
              >
                Ajouter une nouvelle mark
              </button>
              <button
                class="rounded bg-green-500 px-4 py-2 text-white hover:bg-green-600"
                type="button"
                @click="submitData"
              >
                Valider
              </button>
            </div>
          </template>
          <template v-else>
            <div class="flex flex-col gap-4 md:flex-row">
              <button
                class="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
                type="button"
                @click="edit = true"
              >
                Modifier
              </button>
            </div>
          </template>
          <button
            class="rounded bg-purple-500 px-4 py-2 text-white hover:bg-purple-600"
            type="button"
            @click="openGameModal"
          >
            Modifier la répartition par Jeu
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Mark move Modal -->
  <div
    v-if="move"
    class="fixed inset-0 flex items-center justify-center bg-black/50"
  >
    <div
      class="w-1/2 rounded-lg bg-zinc-800 p-4"
    >
      <h2
        class="text-center text-2xl font-bold text-white"
      >
        Déplacer les appareils
      </h2>
      <form
        class="mt-4 flex flex-col gap-4"
        @submit.prevent="validateMove"
      >
        <div
          class="flex flex-row items-center gap-2"
        >
          <div>
            Déplacer les appareils avec la mark
          </div>
          <div
            class="rounded-md bg-theme-nav p-1 font-bold text-white"
          >
            {{ currentMark }}
          </div>
          <div>
            vers la mark :
          </div>
        </div>
        <div
          class="flex flex-col"
        >
          <label
            class="text-white"
            for="mark"
          >
            Nouvelle Mark
          </label>
          <select
            id="mark"
            v-model="chosenMark"
            class="rounded-md border border-black bg-theme-nav p-2 text-white"
          >
            <option
              v-for="mark in marks"
              :key="mark.value"
              :value="mark.value"
            >
              {{ mark.name }} - {{ mark.value }}
            </option>
          </select>
        </div>
        <div
          class="flex justify-end gap-4"
        >
          <button
            class="rounded-md bg-theme-nav px-4 py-2 text-white"
            type="button"
            @click="move = false"
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
      </form>
    </div>
  </div>

  <!-- Game edit Modal-->
  <div
    v-if="game"
    class="fixed inset-0 flex items-center justify-center bg-black/50"
  >
    <div
      class="max-h-[75%] w-1/2 overflow-y-scroll rounded-lg bg-zinc-800 p-4"
    >
      <h2
        class="text-center text-2xl font-bold text-white"
      >
        Modifier la répartition par Jeu
      </h2>
      <div
        class="mt-4 flex flex-row items-center gap-2 border-b-2 border-gray-500 pb-4 text-white"
      >
        Format :
        <div
          class="rounded-md border border-gray-500 bg-theme-nav p-1 font-bold text-white"
        >
          Nom du jeu
        </div> :
        <div
          class="rounded-md border border-black bg-theme-nav p-1 font-bold text-white"
        >
          Mark1,Mark2,...
        </div>
      </div>
      <form
        class="mt-4 flex flex-col gap-4"
        @submit.prevent="submitGame"
      >
        <div
          class="flex flex-col gap-4"
        >
          <template
            v-for="(value, index) in gameMarksFields"
            :key="index"
          >
            <div
              class="flex flex-row items-center justify-between"
            >
              <div
                class="flex flex-row items-center gap-2"
              >
                <label
                  :for="`game-mark-${index}`"
                  class="w-20 overflow-hidden"
                >
                  <input
                    :id="`game-mark-${index}`"
                    v-model="gameMarksFields[index]"
                    class="w-20 truncate rounded-md bg-theme-nav p-1 font-bold text-white"
                  />
                </label>
                <div>
                  :
                </div>
                <input
                  :id="`game-mark-${index}`"
                  v-model="gameMarksValues[index]"
                  class="rounded-md border border-black bg-theme-nav p-2 text-white"
                />
              </div>
              <!-- Supprimer le jeu -->
              <button
                class="rounded-md bg-red-500 p-1 hover:bg-red-600"
                type="button"
                @click="gameMarksFields.splice(index, 1); gameMarksValues.splice(index, 1)"
              >
                <fa-awesome-icon
                  icon="trash-can"
                  size="lg"
                />
              </button>
            </div>
          </template>
          <!-- Ajouter un jeu -->
          <button
            class="rounded-md bg-blue-500 p-1 hover:bg-blue-600"
            type="button"
            @click="gameMarksFields.push(''); gameMarksValues.push('')"
          >
            <fa-awesome-icon
              icon="plus"
              size="lg"
            />
            Ajouter un jeu
          </button>
        </div>
        <div
          class="flex justify-end"
        >
          <button
            class="mr-2 rounded-md bg-theme-nav px-4 py-2 text-white"
            type="button"
            @click="game = false"
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
      </form>
    </div>
  </div>
</template>
