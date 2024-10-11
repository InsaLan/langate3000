<script setup lang="ts">
import { storeToRefs } from 'pinia';
import { onMounted, ref } from 'vue';
import ManagementMenu from '@/components/ManagementMenu.vue';
import type { Mark } from '@/models/mark';
import { useDeviceStore } from '@/stores/devices.store';

const deviceStore = useDeviceStore();

const { fetch_marks, patch_marks } = deviceStore;
const { marks } = storeToRefs(deviceStore);

// make a copy of the marks
const marksCopy = ref<Mark[]>([]);

onMounted(async () => {
  await fetch_marks();
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
              <th class="border-2 border-zinc-800 px-2"/>
            </tr>
          </thead>
          <tbody
            class="text-black"
          >
            <tr
              v-for="(mark, index) in marksCopy"
              :key="index"
              class="border-b"
            >
              <td class="border-2 border-zinc-800 p-2">
                <label class="sr-only" for="name">Name</label>
                <input
                  v-model="mark.name"
                  class="w-full rounded-md border border-black bg-theme-nav p-2 text-white"
                  type="text"
                />
              </td>
              <td class="border-2 border-zinc-800 p-2">
                <label class="sr-only" for="value">Value</label>
                <input
                  v-model.number="mark.value"
                  class="w-full rounded-md border border-black bg-theme-nav p-2 text-white"
                  type="number"
                />
              </td>
              <td class="border-2 border-zinc-800 p-2">
                <label class="sr-only" for="priority">Priority</label>
                <input
                  v-model.number="mark.priority"
                  class="w-full rounded-md border border-black bg-theme-nav p-2 text-white"
                  type="number"
                  step="0.1"
                />
              </td>
              <td class="border-2 border-zinc-800 p-2 text-center">
                <button
                  class="rounded bg-red-500 p-1 text-white hover:bg-red-600"
                  type="button"
                  @click="removeMark(index)"
                >
                  <fa-awesome-icon
                    icon="trash-can"
                    size="lg"
                    class="text-white"
                  />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
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
      </div>
    </div>
  </div>
</template>
