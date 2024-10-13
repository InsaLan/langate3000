import axios, { type AxiosError } from 'axios';
import { defineStore, storeToRefs } from 'pinia';
import { ref } from 'vue';
import type { Device, UserDevice } from '@/models/device';
import type { EditableMark, GameMark, Mark } from '@/models/mark';

import { useNotificationStore } from './notification.stores';
import { useUserStore } from './user.store';

const { get_csrf } = useUserStore();
const { csrf } = storeToRefs(useUserStore());

const { addNotification } = useNotificationStore();

/**
 * This store is used to manage the devices through the API
 * The devices are not stored in the store because of the large amount of data and pagination
 */
export const useDeviceStore = defineStore('device', () => {
  const marks = ref<Mark[]>([] as Mark[]);
  const gameMarks = ref<GameMark>({} as GameMark);

  async function deleteDevice(id: number): Promise<boolean> {
    await get_csrf();
    try {
      await axios.delete(
        `/network/devices/${id}/`,
        {
          headers: {
            'X-CSRFToken': csrf.value,
            'Content-Type': 'application/json',
          },
          withCredentials: true,
        },
      );
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data?.error || 'An error occurred while deleting the device',
        'error',
      );
      return false;
    }
  }

  async function createDevice(data: Device | UserDevice): Promise<boolean> {
    await get_csrf();
    try {
      await axios.post(
        '/network/devices/',
        data,
        {
          headers: {
            'X-CSRFToken': csrf.value,
            'Content-Type': 'application/json',
          },
          withCredentials: true,
        },
      );
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data?.error || 'An error occurred while creating the device',
        'error',
      );
      return false;
    }
  }

  async function createDevicesFromList(data: Device[] | UserDevice[]): Promise<boolean> {
    await get_csrf();
    try {
      await axios.post(
        '/network/devices/',
        data,
        {
          headers: {
            'X-CSRFToken': csrf.value,
            'Content-Type': 'application/json',
          },
          withCredentials: true,
        },
      );
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data?.error || 'An error occurred while creating the devices',
        'error',
      );
      return false;
    }
  }

  async function editDevice(id: number, data: Device | UserDevice): Promise<boolean> {
    await get_csrf();
    try {
      await axios.patch(
        `/network/devices/${id}/`,
        data,
        {
          headers: {
            'X-CSRFToken': csrf.value,
            'Content-Type': 'application/json',
          },
          withCredentials: true,
        },
      );
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data?.error || 'An error occurred while editing the device',
        'error',
      );
      return false;
    }
  }

  async function change_userdevice_marks(data: { [device: string]: string }): Promise<boolean> {
    await get_csrf();

    let errors = false;

    const requests = Object.entries(data).map(([device, mark]) => axios.patch(`/network/devices/${device}/`, { mark }, {
      headers: {
        'X-CSRFToken': csrf.value,
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    }).catch((err) => {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data?.error || 'An error occurred while editing the device',
        'error',
      );
      errors = true;
    }));

    await Promise.all(requests);
    return !errors;
  }

  async function fetch_marks(): Promise<boolean> {
    try {
      const response = await axios.get<Mark[]>('/network/marks/', { withCredentials: true });
      marks.value = response.data;
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data?.error || 'An error occurred while fetching the marks',
        'error',
      );
      return false;
    }
  }

  async function patch_marks(data: EditableMark[]): Promise<boolean> {
    await get_csrf();

    try {
      await axios.patch('/network/marks/', data, {
        headers: {
          'X-CSRFToken': csrf.value,
          'Content-Type': 'application/json',
        },
        withCredentials: true,
      });
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data?.error || 'An error occurred while editing the marks',
        'error',
      );
      return false;
    }
  }

  async function move_marks(oldMark: number, newMark: number): Promise<boolean> {
    await get_csrf();

    try {
      await axios.post(`/network/mark/${oldMark}/move/${newMark}/`, {}, {
        headers: {
          'X-CSRFToken': csrf.value,
          'Content-Type': 'application/json',
        },
        withCredentials: true,
      });
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data?.error || 'An error occurred while moving the marks',
        'error',
      );
      return false;
    }
  }

  async function fetch_game_marks(): Promise<boolean> {
    try {
      const response = await axios.get<GameMark>('/network/games/', { withCredentials: true });
      gameMarks.value = response.data;
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data?.error || 'An error occurred while fetching the game marks',
        'error',
      );
      return false;
    }
  }

  async function change_game_marks(data: GameMark): Promise<boolean> {
    await get_csrf();

    try {
      await axios.patch('/network/games/', data, {
        headers: {
          'X-CSRFToken': csrf.value,
          'Content-Type': 'application/json',
        },
        withCredentials: true,
      });
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data?.error || 'An error occurred while editing the game marks',
        'error',
      );
      return false;
    }
  }

  async function edit_own_device(id: number, name: string): Promise<boolean> {
    await get_csrf();
    try {
      await axios.patch(
        `/network/userdevices/${id}/`,
        { name },
        {
          headers: {
            'X-CSRFToken': csrf.value,
            'Content-Type': 'application/json',
          },
          withCredentials: true,
        },
      );
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data?.error || 'An error occurred while editing the device',
        'error',
      );
      return false;
    }
  }

  async function delete_own_device(id: number): Promise<boolean> {
    await get_csrf();
    try {
      await axios.delete(
        `/network/userdevices/${id}/`,
        {
          headers: {
            'X-CSRFToken': csrf.value,
            'Content-Type': 'application/json',
          },
          withCredentials: true,
        },
      );
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data?.error || 'An error occurred while deleting the device',
        'error',
      );
      return false;
    }
  }

  return {
    marks,
    gameMarks,
    deleteDevice,
    createDevice,
    createDevicesFromList,
    editDevice,
    change_userdevice_marks,
    fetch_marks,
    patch_marks,
    move_marks,
    fetch_game_marks,
    change_game_marks,
    edit_own_device,
    delete_own_device,
  };
}, { persist: false });
