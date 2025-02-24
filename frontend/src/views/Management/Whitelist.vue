<script setup lang="ts">
import ManagementMenu from '@/components/ManagementMenu.vue';
import PaginatedTable from '@/components/PaginatedTable.vue';
import type { Device } from '@/models/device';
import { useDeviceStore } from '@/stores/devices.store';

const {
  createDevice, createDevicesFromList, deleteDevice, editDevice,
} = useDeviceStore();

</script>

<template>
  <div class="m-4 flex flex-col">
    <div class="mb-5 border-b-2 border-gray-500 pb-2 text-4xl font-bold text-gray-300">
      Interface d'administration
    </div>
    <div class="flex flex-col md:flex-row">
      <ManagementMenu type="whitelist"/>
      <PaginatedTable
        url="/network/devices/whitelist/"
        :properties="[
          {
            name: '#',
            key: 'id',
            ordering: true,
          },
          {
            name: 'MAC',
            key: 'mac',
            ordering: false,
          },
          {
            name: 'Nom',
            key: 'name',
            ordering: false,
          },
          {
            name: 'Mark',
            key: 'mark',
            ordering: true,
          },
          {
            name: 'Accès aux sites bloqués',
            key: 'bypass',
            ordering: false,
          },
        ]"
        :pagination="true"
        :search="true"
        :actions="[
          {
            hint: 'Modifier l\'appareil',
            icon: 'pencil',
            key: 'update',
            modal: {
              title: 'Modifier l\'appareil',
              buttons: 'ValiderAnnuler',
              fields: [
                {
                  name: 'Nom',
                  key: 'name',
                  type: 'text',
                  required: true,
                },
                {
                  name: 'MAC',
                  key: 'mac',
                  type: 'text',
                  required: true,
                },
                {
                  name: 'Mark',
                  key: 'mark',
                  type: 'number',
                  required: true,
                },
                {
                  name: 'Donner accès aux sites bloqués',
                  key: 'bypass',
                  type: 'checkbox',
                  required: false,
                },
              ],
            },
            function: async (device, data) => {
              if (await editDevice((device as unknown as Device).id, data as unknown as Device)) {
                return 'L\'appareil a été modifié';
              }
            },
          },
          {
            hint: 'Supprimer l\'appareil',
            icon: 'trash-can',
            key: 'delete',
            modal: {
              title: 'Supprimer l\'appareil',
              buttons: 'ValiderAnnuler',
              fields: [
                {
                  name: 'Voulez-vous vraiment supprimer cet appareil ?',
                  key: 'confirm',
                  type: 'hidden',
                },
              ],
            },
            function: async (device, fields) => {
              if (await deleteDevice((device as unknown as Device).id)) {
                return 'L\'appareil a été supprimé';
              }
            },
          },
          {
            hint: 'Afficher les détails',
            icon: 'info',
            key: 'details',
            modal: {
              title: 'Détails de l\'appareil',
              buttons: 'None',
              additionalUrl: '/network/devices/$(id)/info',
              fields: [
                {
                  name: 'Nom de l\'appareil',
                  key: 'name',
                  type: 'readonly',
                },
                {
                  name: 'Nom d\'hôte',
                  key: 'hostname',
                  type: 'readonly',
                },
                {
                  name: 'Adresse MAC',
                  key: 'mac',
                  type: 'readonly',
                },
                {
                  name: 'Adresse IP',
                  key: 'ip',
                  type: 'readonly',
                },
                {
                  name: 'VLAN',
                  key: 'vlan_name',
                  type: 'readonly',
                },
                {
                  name: 'Mark',
                  key: 'mark',
                  type: 'readonly',
                },
                {
                  name: 'Accès aux sites bloqués',
                  key: 'bypass',
                  type: 'readonly',
                },
                {
                  name: 'Nom du switch',
                  key: 'switch_name',
                  type: 'readonly',
                },
                {
                  name: 'Adresse IP du switch',
                  key: 'switch_ip',
                  type: 'readonly',
                },
                {
                  name: 'Port du switch',
                  key: 'switch_port',
                  type: 'readonly',
                },
              ],
            },
            function: async (device, fields) => { },
          },
        ]"
        :create="{
          multiple: async (data) => {
            if (await createDevicesFromList(data as unknown as Device[])) {
              return 'Les appareils ont été ajoutés';
            }
          },
          modal: {
            title: 'Ajouter à la whitelist',
            buttons: 'ValiderAnnuler',
            fields: [
              {
                name: 'Nom',
                key: 'name',
                type: 'text',
                required: true,
              },
              {
                name: 'MAC',
                key: 'mac',
                type: 'text',
                required: true,
              },
              {
                name: 'Mark',
                key: 'mark',
                type: 'number',
                required: true,
              },
              {
                name: 'Donner accès aux sites bloqués',
                key: 'bypass',
                type: 'checkbox',
                required: false,
              },
            ],
          },
          function: async (data) => {
            if (await createDevice(data as unknown as Device)) {
              return 'L\'appareil a été ajouté';
            }
          },
        }"
      />
    </div>
  </div>
</template>
