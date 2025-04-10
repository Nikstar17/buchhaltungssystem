<template>
  <div>
    <div class="p-6 max-w-4xl mx-auto">
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-gray-800 mb-2">Benutzerprofil bearbeiten</h1>
        <p class="text-gray-600">
          Aktualisieren Sie Ihre persönlichen Informationen und Kontoeinstellungen
        </p>
      </div>

      <!-- Hauptinhalt in Karten -->
      <div class="space-y-6">
        <!-- Persönliche Informationen -->
        <div class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-blue-100 rounded-lg">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-blue-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-gray-800">Persönliche Informationen</h2>
            </div>
          </div>
          <div class="p-6">
            <form @submit.prevent="updatePersonalInfo">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label for="firstName" class="block text-sm font-medium text-gray-700 mb-1"
                    >Vorname</label
                  >
                  <input
                    type="text"
                    id="firstName"
                    v-model="personalInfo.firstName"
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label for="lastName" class="block text-sm font-medium text-gray-700 mb-1"
                    >Nachname</label
                  >
                  <input
                    type="text"
                    id="lastName"
                    v-model="personalInfo.lastName"
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                <div>
                  <label for="email" class="block text-sm font-medium text-gray-700 mb-1"
                    >E-Mail</label
                  >
                  <input
                    type="email"
                    id="email"
                    v-model="personalInfo.email"
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
              </div>
              <div class="mt-6">
                <button
                  type="submit"
                  class="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                  :disabled="isSubmitting"
                >
                  {{ isSubmitting ? 'Wird gespeichert...' : 'Persönliche Daten speichern' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Passwort ändern -->
        <div class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-purple-100 rounded-lg">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-purple-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
                  />
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-gray-800">Passwort ändern</h2>
            </div>
          </div>
          <div class="p-6">
            <form @submit.prevent="updatePassword">
              <div class="space-y-4">
                <div>
                  <label for="currentPassword" class="block text-sm font-medium text-gray-700 mb-1"
                    >Aktuelles Passwort</label
                  >
                  <input
                    type="password"
                    id="currentPassword"
                    v-model="passwordData.currentPassword"
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    required
                  />
                </div>
                <div>
                  <label for="newPassword" class="block text-sm font-medium text-gray-700 mb-1"
                    >Neues Passwort</label
                  >
                  <input
                    type="password"
                    id="newPassword"
                    v-model="passwordData.newPassword"
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    required
                  />
                  <p class="mt-1 text-sm text-gray-500">
                    Mindestens 8 Zeichen, mit Groß- und Kleinbuchstaben, Ziffern und Sonderzeichen
                  </p>
                </div>
                <div>
                  <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-1"
                    >Passwort bestätigen</label
                  >
                  <input
                    type="password"
                    id="confirmPassword"
                    v-model="passwordData.confirmPassword"
                    class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    required
                  />
                </div>
              </div>
              <div class="mt-6">
                <button
                  type="submit"
                  class="px-6 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2"
                  :disabled="isSubmitting || !passwordsMatch || !isPasswordValid"
                >
                  {{ isSubmitting ? 'Wird gespeichert...' : 'Passwort ändern' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Benachrichtigungseinstellungen -->
        <div class="bg-white rounded-xl shadow-md overflow-hidden">
          <div class="p-5 border-b border-gray-100">
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-green-100 rounded-lg">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-green-600"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                  />
                </svg>
              </div>
              <h2 class="text-lg font-semibold text-gray-800">Benachrichtigungseinstellungen</h2>
            </div>
          </div>
          <div class="p-6">
            <form @submit.prevent="updateNotificationSettings">
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-md font-medium text-gray-800">E-Mail-Benachrichtigungen</h3>
                    <p class="text-sm text-gray-500">Erhalten Sie wichtige Updates per E-Mail</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      v-model="notificationSettings.email"
                      class="sr-only peer"
                    />
                    <div
                      class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"
                    ></div>
                  </label>
                </div>
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-md font-medium text-gray-800">Fällige Rechnungen</h3>
                    <p class="text-sm text-gray-500">
                      Benachrichtigungen über bald fällige Rechnungen
                    </p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      v-model="notificationSettings.invoices"
                      class="sr-only peer"
                    />
                    <div
                      class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"
                    ></div>
                  </label>
                </div>
                <div class="flex items-center justify-between">
                  <div>
                    <h3 class="text-md font-medium text-gray-800">System-Updates</h3>
                    <p class="text-sm text-gray-500">Informationen über Systemaktualisierungen</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      v-model="notificationSettings.systemUpdates"
                      class="sr-only peer"
                    />
                    <div
                      class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-green-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"
                    ></div>
                  </label>
                </div>
              </div>
              <div class="mt-6">
                <button
                  type="submit"
                  class="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
                  :disabled="isSubmitting"
                >
                  {{ isSubmitting ? 'Wird gespeichert...' : 'Einstellungen speichern' }}
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Zurück-Button -->
        <div class="mt-6 flex justify-start">
          <RouterLink
            :to="{ name: 'settings' }"
            class="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700 flex items-center space-x-2"
          >
            <ArrowLongLeftIcon class="w-5 h-5" />
            <span>Zurück zu Einstellungen</span>
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { showSnackbarMessage } from '@/composables/useSnackbar';
import { ApiService, AuthService } from '@/services';
import { ArrowLongLeftIcon } from '@heroicons/vue/24/solid';

const router = useRouter();
const userStore = useUserStore();

// Benutzerinformationen
const personalInfo = ref({
  firstName: '',
  lastName: '',
  email: '',
});

// Passwortdaten
const passwordData = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: '',
});

// Benachrichtigungseinstellungen
const notificationSettings = ref({
  email: true,
  invoices: true,
  systemUpdates: false,
});

// Status-Tracking
const isSubmitting = ref(false);

// Computed Properties
const passwordsMatch = computed(() => {
  return passwordData.value.newPassword === passwordData.value.confirmPassword;
});

const isPasswordValid = computed(() => {
  const password = passwordData.value.newPassword;
  // Mindestens 8 Zeichen, ein Großbuchstabe, ein Kleinbuchstabe, eine Zahl und ein Sonderzeichen
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  return passwordRegex.test(password);
});

// Benutzerdaten laden
onMounted(async () => {
  try {
    const userData = await ApiService.get('/api/user');

    personalInfo.value = {
      firstName: userData.first_name || '',
      lastName: userData.last_name || '',
      email: userData.email || '',
      phone: userData.phone || '',
    };

    // Benachrichtigungseinstellungen laden
    if (userData.notification_settings) {
      notificationSettings.value = {
        email: userData.notification_settings.email ?? true,
        invoices: userData.notification_settings.invoices ?? true,
        systemUpdates: userData.notification_settings.system_updates ?? false,
      };
    }
  } catch (error) {
    console.error('Fehler beim Laden der Benutzerdaten:', error);
    showSnackbarMessage('Fehler beim Laden der Benutzerdaten.', 'error');
  }
});

// Persönliche Informationen aktualisieren
const updatePersonalInfo = async () => {
  if (isSubmitting.value) return;
  isSubmitting.value = true;

  try {
    const userData = {
      first_name: personalInfo.value.firstName,
      last_name: personalInfo.value.lastName,
      email: personalInfo.value.email,
      phone: personalInfo.value.phone,
    };

    const response = await ApiService.put('/api/user', userData);

    showSnackbarMessage('Persönliche Informationen wurden erfolgreich aktualisiert.', 'success');

    // Aktualisiere den UserStore mit den neuen Daten
    if (response.user) {
      userStore.setFirstName(response.user.first_name);
      userStore.setLastName(response.user.last_name);
      userStore.setEmail(response.user.email);
    }
  } catch (error) {
    console.error('Fehler beim Aktualisieren der persönlichen Informationen:', error);
    showSnackbarMessage(
      error.message || 'Fehler beim Aktualisieren der persönlichen Informationen.',
      'error'
    );
  } finally {
    isSubmitting.value = false;
  }
};

// Passwort aktualisieren
const updatePassword = async () => {
  if (isSubmitting.value) return;

  // Validierung
  if (!passwordsMatch.value) {
    showSnackbarMessage('Passwörter stimmen nicht überein.', 'error');
    return;
  }

  if (!isPasswordValid.value) {
    showSnackbarMessage('Das Passwort entspricht nicht den Anforderungen.', 'error');
    return;
  }

  isSubmitting.value = true;
  try {
    const passwordUpdateData = {
      current_password: passwordData.value.currentPassword,
      new_password: passwordData.value.newPassword,
    };

    await AuthService.changePassword(passwordUpdateData);

    showSnackbarMessage('Passwort wurde erfolgreich aktualisiert.', 'success');

    // Passwortfelder zurücksetzen
    passwordData.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: '',
    };
  } catch (error) {
    console.error('Fehler beim Aktualisieren des Passworts:', error);
    showSnackbarMessage(error.message || 'Fehler beim Aktualisieren des Passworts.', 'error');
  } finally {
    isSubmitting.value = false;
  }
};

// Benachrichtigungseinstellungen aktualisieren
const updateNotificationSettings = async () => {
  if (isSubmitting.value) return;

  isSubmitting.value = true;
  try {
    await ApiService.put('/api/user/notifications', {
      notification_settings: {
        email: notificationSettings.value.email,
        invoices: notificationSettings.value.invoices,
        system_updates: notificationSettings.value.systemUpdates,
      },
    });

    showSnackbarMessage(
      'Benachrichtigungseinstellungen wurden erfolgreich aktualisiert.',
      'success'
    );
  } catch (error) {
    console.error('Fehler beim Aktualisieren der Benachrichtigungseinstellungen:', error);
    showSnackbarMessage(
      error.message || 'Fehler beim Aktualisieren der Benachrichtigungseinstellungen.',
      'error'
    );
  } finally {
    isSubmitting.value = false;
  }
};

// Zurück zur Einstellungsübersicht
const goBack = () => {
  router.push({ name: 'settings' });
};
</script>

<style scoped>
/* Zusätzliche benutzerdefinierte Stile können hier hinzugefügt werden */
</style>
