import axios, { type AxiosError } from 'axios';
import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import type { User } from '@/models/user';
import { wordList } from '@/utils/wordList';

import { useNotificationStore } from './notification.stores';

export const useUserStore = defineStore('user', () => {
  const user = ref<User>({} as User);
  const isConnected = ref(false);
  const csrf = ref('');
  const connectionTimestamp = ref(0);
  const router = useRouter();
  const { addNotification } = useNotificationStore();

  function create_temp_password(): string {
    // Create a password using two random words
    const random1 = Math.floor(Math.random() * wordList.length);
    const random2 = Math.floor(Math.random() * wordList.length);
    const password = `${wordList[random1]}-${wordList[random2]}`;
    return password;
  }

  /*
  * Get a new csrf token from the server
  */
  async function get_csrf() {
    await axios.get('/user/get-csrf/');
    let cookie = '';
    document.cookie.split(';').forEach((cookie_value) => {
      if (cookie_value.split('=')[0].trim() === 'csrftoken') {
        cookie = cookie_value.split('=')[1].trim();
      }
    });
    csrf.value = cookie;
  }

  async function login(username: string, password: string): Promise<boolean> {
    await get_csrf();

    try {
      const user_data = await axios.post<User>('/user/login/', { username, password }, {
        headers: {
          'X-CSRFToken': csrf.value,
          'Content-Type': 'application/json',
        },
        withCredentials: true,
      });

      user.value = user_data.data;
      isConnected.value = true;
      connectionTimestamp.value = Date.now();
      await router.push('/');
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data || 'An error occurred while logging in',
        'error',
      );
      return false;
    }
  }

  async function logout(): Promise<boolean> {
    await get_csrf();

    try {
      await axios.post('/user/logout/', {}, {
        headers: {
          'X-CSRFToken': csrf.value,
          'Content-Type': 'application/json',
        },
        withCredentials: true,
      });
      isConnected.value = false;
      await router.push('/login');
      user.value = {} as User;
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data || 'An error occurred while logging out',
        'error',
      );
      return false;
    }
  }

  async function handle_session_cookie_expiration() {
    const now = Date.now();
    if (
      isConnected.value
      && now - connectionTimestamp.value
      > import.meta.env.VITE_SESSION_COOKIE_AGE * 1000
    ) {
      await logout();
      await router.push('/login');
    }
  }

  async function create_user(data: User): Promise<boolean> {
    await get_csrf();

    try {
      await axios.post('/user/users/', data, {
        headers: {
          'X-CSRFToken': csrf.value,
          'Content-Type': 'application/json',
        },
        withCredentials: true,
      });
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data || 'An error occurred while creating the user',
        'error',
      );
      return false;
    }
  }

  async function reset_password(id: number, password: string): Promise<boolean> {
    await get_csrf();

    try {
      await axios.post(`/user/change-password/${id}/`, { password }, {
        headers: {
          'X-CSRFToken': csrf.value,
          'Content-Type': 'application/json',
        },
        withCredentials: true,
      });
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data || 'An error occurred while resetting the password',
        'error',
      );
      return false;
    }
  }

  async function delete_user(id: number): Promise<boolean> {
    await get_csrf();

    try {
      await axios.delete(`/user/users/${id}/`, {
        headers: {
          'X-CSRFToken': csrf.value,
          'Content-Type': 'application/json',
        },
        withCredentials: true,
      });
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data || 'An error occurred while deleting the user',
        'error',
      );
      return false;
    }
  }

  async function edit_user(id: number, data: User): Promise<boolean> {
    await get_csrf();

    try {
      await axios.patch(`/user/users/${id}/`, data, {
        headers: {
          'X-CSRFToken': csrf.value,
          'Content-Type': 'application/json',
        },
        withCredentials: true,
      });
      return true;
    } catch (err) {
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data || 'An error occurred while editing the user',
        'error',
      );
      return false;
    }
  }

  async function fetch_user(): Promise<boolean> {
    try {
      const user_data = await axios.get<User>('/user/me/', {
        withCredentials: true,
      });
      user.value = user_data.data;
      isConnected.value = true;

      return true;
    } catch (err) {
      if ((err as AxiosError).response?.status === 403) {
        isConnected.value = false;

        // clear user data
        user.value = {} as User;

        await router.push('/login');
        return false;
      }
      addNotification(
        (err as AxiosError<{ error?: string }>).response?.data || 'An error occurred while fetching the user',
        'error',
      );
      return false;
    }
  }

  return {
    user,
    login,
    logout,
    get_csrf,
    handle_session_cookie_expiration,
    create_user,
    create_temp_password,
    reset_password,
    delete_user,
    edit_user,
    fetch_user,
    isConnected,
    csrf,
    connectionTimestamp,
  };
}, { persist: true });
