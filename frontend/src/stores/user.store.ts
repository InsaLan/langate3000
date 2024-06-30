import axios, { type AxiosError } from 'axios';
import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import type { User } from '@/models/user';

export const useUserStore = defineStore('user', () => {
  const user = ref<User>({} as User);
  const isConnected = ref(false);
  const csrf = ref('');
  const connectionTimestamp = ref(0);
  const router = useRouter();

  function create_temp_password(): string {
    // create a 4 digits password
    const password = Math.floor(Math.random() * 9999).toString();
    // Ensure that the password is a string of 4 digits
    return password.padStart(4, '0');
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

  async function login(username: string, password: string): Promise<string | undefined> {
    await get_csrf();

    try {
      await axios.post('/user/login/', { username, password }, {
        headers: {
          'X-CSRFToken': csrf.value,
          'Content-Type': 'application/json',
        },
        withCredentials: true,
      });

      const user_data = await axios.get<User>('/user/me/', { withCredentials: true });
      user.value = user_data.data;
      isConnected.value = true;
      connectionTimestamp.value = Date.now();
      await router.push('/');
      return undefined;
    } catch (err) {
      return ((err as AxiosError<{ user: string[] }>).response?.data?.user?.[0]);
    }
  }

  async function logout() {
    await axios.post('/user/logout/', {}, {
      headers: {
        'X-CSRFToken': csrf.value,
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    });
    isConnected.value = false;
    user.value = {} as User;
    await router.push('/login');
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

  async function create_user(data: User): Promise<void> {
    await get_csrf();

    try {
      await axios.post('/user/users/', data, {
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

  async function reset_password(id: number): Promise<string | undefined> {
    await get_csrf();

    const password = create_temp_password();

    try {
      await axios.post(`/user/change-password/${id}/`, { password }, {
        headers: {
          'X-CSRFToken': csrf.value,
          'Content-Type': 'application/json',
        },
        withCredentials: true,
      });
      return password;
    } catch (err) {
      // TODO : display error message with a component
      console.error((err as AxiosError).response?.data);
      return undefined;
    }
  }

  async function delete_user(id: number): Promise<void> {
    await get_csrf();

    try {
      await axios.delete(`/user/users/${id}/`, {
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

  async function edit_user(id: number, data: User): Promise<void> {
    await get_csrf();

    try {
      await axios.patch(`/user/users/${id}/`, data, {
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
    isConnected,
    csrf,
    connectionTimestamp,
  };
}, { persist: true });
