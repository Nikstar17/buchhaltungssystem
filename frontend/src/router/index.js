import { createRouter, createWebHistory } from 'vue-router';
import { jwtDecode } from 'jwt-decode';
import RegisterComp from '@/views/auth/RegisterView.vue';
import LoginView from '@/views/auth/LoginView.vue';
import BaseLayout from '@/views/dashboard/BaseLayout.vue'; // Umbenannt von DashboardView.vue
import DashboardOverview from '@/components/dashboard/DashboardOverview.vue'; // Umbenannt von HomeComp.vue
import DocumentsList from '@/components/documents/DocumentList.vue';
import DocumentDetails from '@/components/documents/DocumentDetail.vue';
import DocumentForm from '@/components/documents/DocumentForm.vue';
import JournalEntryList from '@/components/journalEntries/JournalEntryList.vue';
import JournalEntryForm from '@/components/journalEntries/JournalEntryForm.vue';
import API_URL from '@/api';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/register',
      name: 'register',
      component: RegisterComp,
    },
    {
      path: '/',
      name: 'root',
      component: LoginView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
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
      component: BaseLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'overview', // Neuer Pfadname
          name: 'dashboard-overview', // Neuer Name
          component: DashboardOverview, // Neuer Name für die Komponente
        },
        {
          path: 'documents',
          name: 'documents',
          component: DocumentsList,
        },
        {
          path: '/documents/:id',
          component: DocumentDetails,
        },
        {
          path: 'documents/form',
          name: 'document-form',
          component: DocumentForm,
        },
        {
          path: 'journalentry',
          name: 'journal-entry',
          component: JournalEntryList,
        },
        {
          path: 'journalentry/form',
          name: 'journal-entry-form',
          component: JournalEntryForm,
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
