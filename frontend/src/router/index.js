import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { jwtDecode } from 'jwt-decode';
import RegisterComp from '@/views/RegisterView.vue';
import LoginPage from '@/views/LoginView.vue';
import DashboardView from '@/views/DashboardView.vue';
import DashboardComp from '@/components/HomeComp.vue';
import DocumentsComp from '@/components/DocumentsComp.vue';
import DocumentDetails from '@/components/DocumentDetails.vue';
import DocumentUpload from '@/components/DocumentUpload.vue';
import API_URL from '@/api';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {},
    {
      path: '/register',
      name: 'register',
      component: RegisterComp,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
    },
    {
      path: '/logout',
      name: 'logout',
      beforeEnter: (to, from, next) => {
        localStorage.removeItem('access_token');
        next({ name: 'login' });
      },
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
          component: DashboardComp,
        },
        {
          path: 'documents',
          name: 'documents',
          component: DocumentsComp,
        },
        {
          path: '/documents/:id',
          component: DocumentDetails,
        },
        {
          path: 'documents/upload',
          name: 'document-upload',
          component: DocumentUpload,
        },
      ],
    },
  ],
});

// Navigation Guard
router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    const tokenExp = localStorage.getItem('access_token_exp');
    const now = Date.now();

    if (tokenExp && now < tokenExp) {
      next(); // Token is still valid
    } else {
      try {
        const csrfToken = document.cookie
          .split('; ')
          .find((row) => row.startsWith('csrf_refresh_token='))
          ?.split('=')[1];

        if (!csrfToken) {
          console.error('CSRF-Token fehlt.');
          next({ name: 'login' });
          return;
        }

        const response = await fetch(`${API_URL}/refresh`, {
          method: 'POST',
          credentials: 'include',
          headers: {
            'X-CSRF-TOKEN': csrfToken,
          },
        });

        if (response.ok) {
          const data = await response.json();
          const decodedToken = jwtDecode(data.access_token);
          localStorage.setItem('access_token_exp', decodedToken.exp * 1000); // Update expiration time
          next();
        } else {
          console.error('Token konnte nicht erneuert werden. Redirecting to login.');
          next({ name: 'login' });
        }
      } catch (error) {
        console.error('Fehler bei der Token-Erneuerung:', error);
        next({ name: 'login' });
      }
    }
  } else {
    next();
  }
});

export default router;
