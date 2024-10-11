import axios, { type AxiosError } from 'axios';
import { defineStore, storeToRefs } from 'pinia';
import { ref } from 'vue';
import type { Device, UserDevice } from '@/models/device';
import type { Mark } from '@/models/mark';

import { useUserStore } from './user.store';

const { get_csrf } = useUserStore();
const { csrf } = storeToRefs(useUserStore());

/**
 * This store is used to manage the devices through the API
 * The devices are not stored in the store because of the large amount of data and pagination
 */
export const useDeviceStore = defineStore('device', () => {
  const marks = ref<Mark[]>([] as Mark[]);

  async function deleteDevice(id: number): Promise<void> {
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
    } catch (err) {
      // TODO : display error message with a component
      console.error((err as AxiosError).response?.data);
    }
  }

  async function createDevice(data: Device | UserDevice): Promise<void> {
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
    } catch (err) {
      // TODO : display error message with a component
      console.error((err as AxiosError).response?.data);
    }
  }

  async function createDevicesFromList(data: Device[] | UserDevice[]): Promise<void> {
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
    } catch (err) {
      // TODO : display error message with a component
      console.error((err as AxiosError).response?.data);
    }
  }

  async function editDevice(id: number, data: Device | UserDevice): Promise<void> {
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
    } catch (err) {
      // TODO : display error message with a component
      console.error((err as AxiosError).response?.data);
    }
  }

  async function change_userdevice_marks(data: { [device: string]: string }): Promise<void> {
    await get_csrf();

    const requests = Object.entries(data).map(([device, mark]) => axios.patch(`/network/devices/${device}/`, { mark }, {
      headers: {
        'X-CSRFToken': csrf.value,
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    }).catch((err) => {
      // TODO : handle error appropriately
      console.error((err as AxiosError).response?.data);
    }));

    await Promise.all(requests);
  }

  async function fetch_marks(): Promise<void> {
    try {
      const response = await axios.get<Mark[]>('/network/marks/', { withCredentials: true });
      marks.value = response.data;
    } catch (err) {
      // TODO : display error message with a component
      console.error((err as AxiosError).response?.data);
    }
  }

  async function patch_marks(data: Mark[]): Promise<void> {
    await get_csrf();

    try {
      await axios.patch('/network/marks/', data, {
        headers: {
          'X-CSRFToken': csrf.value,
          'Content-Type': 'application/json',
        },
        withCredentials: true,
      });
    } catch (err) {
      // TODO : display error message with a component
      console.error((err as AxiosError).response?.data);
    }
  }

  return {
    marks,
    deleteDevice,
    createDevice,
    createDevicesFromList,
    editDevice,
    change_userdevice_marks,
    fetch_marks,
    patch_marks,
  };
}, { persist: false });
