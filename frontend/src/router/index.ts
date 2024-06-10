import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
import { useUserStore } from '@/stores/user.store';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/views/Home.vue'),
    beforeEnter: () => {
      const { isConnected } = useUserStore();
      return !isConnected ? { path: '/login' } : true;
    },
  },
  {
    path: '/login',
    component: () => import('@/views/Login.vue'),
  },
  {
    path: '/:pathMatch(.*)*',
    component: () => import('@/views/NotFound.vue'),
  },
];

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    return { top: 0 };
  },
});
