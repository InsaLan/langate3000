<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { onMounted, ref } from 'vue';
import ManagementMenu from '@/components/ManagementMenu.vue';
import type { EditableMark, Mark } from '@/models/mark';
import { useDeviceStore } from '@/stores/devices.store';

const deviceStore = useDeviceStore();

const { fetch_marks, patch_marks } = deviceStore;
const { marks } = storeToRefs(deviceStore);

const marksCopy = ref<EditableMark[]>([]);

const edit = ref(false);

onMounted(async () => {
  await fetch_marks();
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
  await patch_marks(marksCopy.value);
  // TODO: display a success message
  console.log('Data submitted');
};

const reset = async () => {
  marksCopy.value = marks.value.map((mark) => ({ ...mark }));
  edit.value = false;
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
                    <label class="sr-only" for="priority">Priority</label>
                    <input
                      v-model.number="mark.priority"
                      class="w-full rounded-md border border-black bg-theme-nav p-2"
                      type="number"
                      step="0.1"
                    />
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
                <td class="border-2 border-zinc-800 p-2 text-center">
                  <template v-if="edit">
                    <button
                      class="rounded bg-red-500 p-1 hover:bg-red-600"
                      type="button"
                      @click="removeMark(index)"
                    >
                      <fa-awesome-icon
                        icon="trash-can"
                        size="lg"
                      />
                    </button>
                  </template>
                  <template v-else>
                    <!--
                      Add different actions here :
                      - View devices with this mark
                      - Change devices with this mark to another mark
                      - ...
                    -->
                    <div>
                      TODO
                    </div>
                  </template>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <template v-if="edit">
          <div class="mt-4 space-x-4">
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
          <div class="mt-4 space-x-4">
            <button
              class="rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600"
              type="button"
              @click="edit = true"
            >
              Modifier
            </button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>
