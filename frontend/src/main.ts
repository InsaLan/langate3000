import { library } from '@fortawesome/fontawesome-svg-core';
import {
  faArrowLeft,
  faArrowsRotate, faBolt, faChevronDown, faChevronUp,
  faCircle, faCircleCheck, faCirclePlus, faClock,
  faCrown,
  faDownload, faEye, faEyeSlash,
  faFile, faHammer, faMagnifyingGlass, faPencil, faTrashCan, faWarning,
} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import axios, { type AxiosError } from 'axios';
import { createPinia } from 'pinia';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import { createApp } from 'vue';
import Multiselect from 'vue-multiselect';
import { router } from '@/router';

import App from './App.vue';

import './style.css';

/* add icons to the library */
library.add(
  faCirclePlus,
  faPencil,
  faWarning,
  faFile,
  faArrowsRotate,
  faCircleCheck,
  faCircle,
  faClock,
  faEye,
  faEyeSlash,
  faChevronDown,
  faChevronUp,
  faDownload,
  faMagnifyingGlass,
  faTrashCan,
  faBolt,
  faArrowLeft,
  faHammer,
  faCrown,
);

axios.defaults.baseURL = import.meta.env.VITE_API_URL;
axios.defaults.withCredentials = true;

const pinia = createPinia();

pinia.use(piniaPluginPersistedstate);

createApp(App)
  .component('multiselect', Multiselect)
  .component('fa-awesome-icon', FontAwesomeIcon)
  .use(pinia)
  .use(router)
  .mount('#app');

axios.interceptors.response.use(
  (res) => res,
  (error: AxiosError<string | { [key: string]: string }, unknown>) => {
    if (typeof error.response?.data === 'string') {
      console.error(error.response.data);
    } else if (typeof error.response?.data === 'object') {
      Object.values(error.response.data).forEach((val) => {
        if (typeof val === 'object') {
          Object.values(val)
            .filter((item): item is string => typeof item === 'string')
            .forEach((item) => console.error(item));
        } else {
          console.error(val);
        }
      });
    } else {
      console.error(error);
    }
    return Promise.reject(error);
  },
);
