import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
import { UserRole } from '@/models/user';
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
    path: '/faq',
    component: () => import('@/views/FAQ.vue'),
  },
  {
    path: '/management/users',
    component: () => import('@/views/Management/Users.vue'),
    beforeEnter: () => {
      const { isConnected, user } = useUserStore();
      return !isConnected || (
        user.role !== UserRole.Admin
        && user.role !== UserRole.Staff
      ) ? { path: '/' } : true;
    },
  },
  {
    path: '/management/marks',
    component: () => import('@/views/Management/Marks.vue'),
    beforeEnter: () => {
      const { isConnected, user } = useUserStore();
      return !isConnected || (
        user.role !== UserRole.Admin
        && user.role !== UserRole.Staff
      ) ? { path: '/' } : true;
    },
  },
  {
    path: '/management/devices',
    component: () => import('@/views/Management/Devices.vue'),
    beforeEnter: () => {
      const { isConnected, user } = useUserStore();
      return !isConnected || (
        user.role !== UserRole.Admin
        && user.role !== UserRole.Staff
      ) ? { path: '/' } : true;
    },
  },
  {
    path: '/management/whitelist',
    component: () => import('@/views/Management/Whitelist.vue'),
    beforeEnter: () => {
      const { isConnected, user } = useUserStore();
      return !isConnected || (
        user.role !== UserRole.Admin
        && user.role !== UserRole.Staff
      ) ? { path: '/' } : true;
    },
  },
  {
    path: '/management/announces',
    component: () => import('@/views/Management/Announces.vue'),
    beforeEnter: () => {
      const { isConnected, user } = useUserStore();
      return !isConnected || (
        user.role !== UserRole.Admin
        && user.role !== UserRole.Staff
      ) ? { path: '/' } : true;
    },
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
