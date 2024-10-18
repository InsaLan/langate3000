<script setup lang="ts">
import ManagementMenu from '@/components/ManagementMenu.vue';
import PaginatedTable from '@/components/PaginatedTable.vue';
import type { Device } from '@/models/device';
import type { User } from '@/models/user';
import { UserRole } from '@/models/user';
import { useDeviceStore } from '@/stores/devices.store';
import { useUserStore } from '@/stores/user.store';

const {
  create_user, reset_password, delete_user, edit_user,
} = useUserStore();

const {
  change_userdevice_marks,
} = useDeviceStore();

</script>

<template>
  <div class="m-4 flex flex-col">
    <div class="mb-5 border-b-2 border-gray-500 pb-2 text-4xl font-bold text-gray-300">
      Interface d'administration
    </div>
    <div class="flex flex-col md:flex-row">
      <ManagementMenu type="users"/>
      <PaginatedTable
        url="/user/users"
        :properties="[
          {
            name: '#',
            key: 'id',
            ordering: true,
          },
          {
            name: 'Pseudo',
            key: 'username',
            ordering: false,
          },
          {
            name: 'Role',
            key: 'role',
            ordering: false,
          },
          {
            name: 'Nombre d\'appareils connectés',
            key: 'device_nb',
            ordering: true,
            function: (user: unknown) => (user as User).devices.length.toString(),
          },
          {
            name: 'Nombre max d\'appareils',
            key: 'max_device_nb',
            ordering: true,
          },
          {
            name: 'Tournois',
            key: 'tournaments',
            ordering: false,
          },
          {
            name: 'Equipe',
            key: 'team',
            ordering: false,
          },
        ]"
        :create="{
          modal: {
            title: 'Ajouter un utilisateur',
            fields: [
              {
                name: 'Pseudo',
                key: 'username',
                type: 'text',
                required: true,
              },
              {
                name: 'Role',
                key: 'role',
                type: 'text',
                required: true,
                choices: [
                  {
                    key: UserRole.Player,
                    value: 'Joueur',
                  },
                  {
                    key: UserRole.Manager,
                    value: 'Manager',
                  },
                  {
                    key: UserRole.Guest,
                    value: 'Invité',
                  },
                  {
                    key: UserRole.Staff,
                    value: 'Staff',
                  },
                  {
                    key: UserRole.Admin,
                    value: 'Admin',
                  },
                ],
              },
              {
                name: 'Mot de passe',
                key: 'password',
                type: 'password',
                required: true,
              },
              {
                name: 'Tournois',
                key: 'tournaments',
                type: 'text',
                required: false,
              },
              {
                name: 'Equipe',
                key: 'team',
                type: 'text',
                required: false,
              },
            ],
          },
          function: async (data) => {
            const password = await create_user(data as unknown as User);
          },
        }"
        :pagination="true"
        :search="true"
        :actions="[
          {
            hint: 'Modifier l\'utilisateur',
            icon: 'pencil',
            key: 'update',
            modal: {
              title: 'Modifier l\'utilisateur',
              fields: [
                {
                  name: 'Pseudo',
                  key: 'username',
                  type: 'text',
                },
                {
                  name: 'Nombre d\'appareils autorisés',
                  key: 'max_device_nb',
                  type: 'number',
                },
                {
                  name: 'Role',
                  key: 'role',
                  type: 'text',
                  choices: [
                    {
                      key: UserRole.Player,
                      value: 'Joueur',
                    },
                    {
                      key: UserRole.Manager,
                      value: 'Manager',
                    },
                    {
                      key: UserRole.Guest,
                      value: 'Invité',
                    },
                    {
                      key: UserRole.Staff,
                      value: 'Staff',
                    },
                    {
                      key: UserRole.Admin,
                      value: 'Admin',
                    },
                  ],
                },
                {
                  name: 'Tournois',
                  key: 'tournaments',
                  type: 'text',
                },
                {
                  name: 'Equipe',
                  key: 'team',
                  type: 'text',
                },
              ],
            },
            function: async (device, fields) => {
              await edit_user((device as unknown as User).id, fields as unknown as User);
            },
          },
          {
            hint: 'Réinitialiser le mot de passe',
            icon: 'key',
            key: 'reset',
            modal: {
              title: 'Réinitialiser le mot de passe',
              fields: [
                {
                  name: 'Voulez-vous vraiment réinitialiser le mot de passe de cet utilisateur ?',
                  key: 'confirm',
                  type: 'hidden',
                },
              ],
            },
            function: async (device, fields) => {
              const password = await reset_password((device as unknown as User).id);
              return 'Le mot de passe a bien été réinitialisé, le nouveau mot de passe est : ' + password;
            },
          },
          {
            hint: 'Modifier les marks',
            icon: 'location-dot',
            key: 'devices',
            modal: {
              title: 'Modifier les marks',
              fields: (devices: unknown) => {
                return (devices as Device[]).map((device: any) => ({
                  name: 'Mark de ' + device.name + (' (' + device.ip + ')'),
                  key: device.id,
                  type: 'number',
                  value: device.mark,
                  required: true,
                  device,
                }));
              },
            },
            function: async (user, fields) => {
              await change_userdevice_marks(fields);
            },
          },
          {
            hint: 'Supprimer l\'utilisateur',
            icon: 'trash-can',
            key: 'delete',
            modal: {
              title: 'Supprimer l\'utilisateur',
              fields: [
                {
                  name: 'Voulez-vous vraiment supprimer cet utilisateur ?',
                  key: 'confirm',
                  type: 'hidden',
                },
              ],
            },
            function: async (device, fields) => {
              await delete_user((device as unknown as User).id);
              return 'l\'utilisateur a été supprimé';
            },
          },
        ]"
      />
    </div>
  </div>
</template>
