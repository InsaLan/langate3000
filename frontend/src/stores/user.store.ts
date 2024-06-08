import axios from 'axios';
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

  async function login(username: string, password: string) {
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
    } catch (err) {
      console.error(err);
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

  return {
    user,
    login,
    logout,
    get_csrf,
    handle_session_cookie_expiration,
    isConnected,
    csrf,
    connectionTimestamp,
  };
}, { persist: true });
