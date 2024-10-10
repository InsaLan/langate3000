import axios, { type AxiosError } from 'axios';
import { defineStore, storeToRefs } from 'pinia';
import type { Device, UserDevice } from '@/models/device';

import { useUserStore } from './user.store';

const { get_csrf } = useUserStore();
const { csrf } = storeToRefs(useUserStore());

/**
 * This store is used to manage the devices through the API
 * The devices are not stored in the store because of the large amount of data and pagination
 */
export const useDeviceStore = defineStore('device', () => {
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

  return {
    deleteDevice,
    createDevice,
    createDevicesFromList,
    editDevice,
    change_userdevice_marks,
  };
}, { persist: false });
