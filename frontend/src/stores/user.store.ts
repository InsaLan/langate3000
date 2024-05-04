import axios from 'axios';
import { defineStore } from 'pinia';
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import type { User } from '@/models/user';

export const useUserStore = defineStore('user', () => {
  const user = ref<User>({} as User);
  const isConnected = ref(false);
  const csrf = ref('');
  const connectionTimestamp = ref(0);
  const router = useRouter();
  const MailVerified = ref(false);

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

  async function signin(
    email: string,
    username: string,
    password: string,
    password_validation: string,
    decoy?: string,
  ) {
    await get_csrf();
    const data = {
      username,
      email,
      password,
      password_validation,
      decoy,
    };
    await axios.post('/user/register/', data, {
      headers: {
        'X-CSRFToken': csrf.value,
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    });
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
      await router.push('/me');
    } catch (err) {
      /* empty */
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
      await router.push('/register');
    }
  }

  const role = computed(() => {
    if (user.value.is_superuser) return 'dev';
    if (user.value.is_staff) return 'staff';
    return 'joueur';
  });

  return {
    user,
    signin,
    login,
    logout,
    get_csrf,
    handle_session_cookie_expiration,
    role,
    isConnected,
    MailVerified,
    csrf,
    connectionTimestamp,
  };
}, { persist: true });
