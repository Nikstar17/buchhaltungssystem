import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/user';
import DashboardView from '@/views/DashboardView.vue';
import LoginPage from '@/views/LoginView.vue';
import RegisterComp from '@/views/RegisterView.vue';
import DocumentsComp from '@/components/DocumentsComp.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/register',
      name: 'register',
      component: RegisterComp
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage
    },
    {
      path: '/logout',
      name: 'logout',
      beforeEnter: (to, from, next) => {
        localStorage.removeItem('access_token');
        next({ name: 'login' });
      }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'home',
          name: 'home',
          component: DashboardComp
        },
        {
          path: 'documents',
          name: 'documents',
          component: DocumentsComp
        }
      ]
    }
  ]
});

import API_URL from '@/api';
import DashboardComp from '@/components/HomeComp.vue';

// Navigation Guard
router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const token = localStorage.getItem('access_token');
    const userStore = useUserStore();

    if (!token) {
      next({ name: 'login' });
      return;
    }

    try {
      const response = await fetch(`${API_URL}/user`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        }
      });

      if (response.ok) {
        const userInfo = await response.json();
        userStore.setEmail(userInfo.email);
        userStore.setId(userInfo.id);
        next();
      } else if (response.status === 401) {
        console.error('Token abgelaufen. Redirecting to login.');
        localStorage.removeItem('access_token');
        next({ name: 'login' });
      } else {
        console.error('Unauthorized. Redirecting to login.');
        localStorage.removeItem('access_token');
        next({ name: 'login' });
      }
    } catch (error) {
      console.error('Fehler bei der Token-Überprüfung:', error);
      localStorage.removeItem('access_token');
      next({ name: 'login' });
    }
  } else {
    next();
  }
});

export default router;
