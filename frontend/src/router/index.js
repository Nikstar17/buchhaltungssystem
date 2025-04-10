import { createRouter, createWebHistory } from 'vue-router';
import { jwtDecode } from 'jwt-decode';
import AuthService from '@/services/auth.service';
import RegisterComp from '@/views/auth/RegisterView.vue';
import LoginView from '@/views/auth/LoginView.vue';
import BaseLayout from '@/views/dashboard/BaseLayout.vue';
import DashboardOverview from '@/components/dashboard/DashboardOverview.vue';
import DocumentsList from '@/components/documents/DocumentList.vue';
import DocumentDetails from '@/components/documents/DocumentDetail.vue';
import DocumentForm from '@/components/documents/DocumentForm.vue';
import JournalEntryList from '@/components/journalEntries/JournalEntryList.vue';
import JournalEntryForm from '@/components/journalEntries/JournalEntryForm.vue';
import SettingsOverview from '@/components/settings/SettingsOverview.vue';
import UserSettings from '@/components/settings/UserSettings.vue';
import ChartOfAccountsSettings from '@/components/settings/ChartOfAccountsSettings.vue';

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
        AuthService.logout();
        next({ name: 'login' });
      },
    },
    {
      path: '/dashboard',
      component: BaseLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          name: 'dashboard', // Name wurde zur Default-Route verschoben
          redirect: { name: 'dashboard-overview' },
        },
        {
          path: 'overview',
          name: 'dashboard-overview',
          component: DashboardOverview,
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
        {
          path: 'settings',
          name: 'settings',
          component: SettingsOverview,
        },
        {
          path: 'settings/profile',
          name: 'user-settings',
          component: UserSettings,
        },
        {
          path: 'settings/chart-of-accounts',
          name: 'settings-chart-of-accounts',
          component: ChartOfAccountsSettings,
        },
      ],
    },
    // Fallback-Route für nicht gefundene Pfade
    {
      path: '/:pathMatch(.*)*',
      redirect: { name: 'login' },
    },
  ],
});

// Navigation Guard
router.beforeEach(async (to, from, next) => {
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    // Prüfen, ob Token vorhanden und gültig ist
    if (AuthService.isLoggedIn() && !AuthService.isTokenExpired()) {
      return next();
    }

    // Wenn Token vorhanden aber abgelaufen, versuche Refresh
    if (AuthService.isLoggedIn()) {
      try {
        await AuthService.refreshToken();
        // Nach Refresh direkt weitergehen
        return next();
      } catch (error) {
        console.error('Token konnte nicht aktualisiert werden:', error);
        return next({ name: 'login' });
      }
    }

    // Kein Token vorhanden, zur Login-Seite weiterleiten
    return next({ name: 'login' });
  } else {
    next();
  }
});

export default router;
