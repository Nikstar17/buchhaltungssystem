<template>
  <div class="p-6 bg-gray-50 text-gray-800">
    <form @submit.prevent="submitJournalEntry" class="bg-white p-6 rounded-xl shadow-sm space-y-6">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold text-gray-800">Neue Buchung</h2>
        <button
          type="submit"
          class="px-5 py-2.5 rounded-xl shadow-md bg-blue-600 text-white hover:bg-blue-700 transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        >
          Buchung erstellen
        </button>
      </div>

      <div class="grid grid-cols-2 gap-5">
        <div class="space-y-2">
          <label for="entry_date" class="block text-sm font-semibold text-gray-700">
            Datum *
          </label>
          <input
            type="date"
            id="entry_date"
            v-model="journalEntry.entry_date"
            required
            class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
          />
        </div>

        <div class="space-y-2">
          <label for="document_number" class="block text-sm font-semibold text-gray-700">
            Belegnummer *
          </label>
          <input
            type="text"
            id="document_number"
            v-model="journalEntry.document_number"
            required
            placeholder="Belegnummer eingeben"
            class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
          />
        </div>
      </div>

      <div class="grid grid-cols-2 gap-5">
        <div class="space-y-2">
          <label for="debit_account" class="block text-sm font-semibold text-gray-700">
            Konto Soll *
          </label>
          <input
            type="text"
            id="debit_account"
            v-model="journalEntry.debit_account"
            required
            placeholder="Konto-Nr. eingeben"
            class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
          />
        </div>

        <div class="space-y-2">
          <label for="credit_account" class="block text-sm font-semibold text-gray-700">
            Konto Haben *
          </label>
          <input
            type="text"
            id="credit_account"
            v-model="journalEntry.credit_account"
            required
            placeholder="Konto-Nr. eingeben"
            class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
          />
        </div>
      </div>

      <div class="space-y-2">
        <label for="amount" class="block text-sm font-semibold text-gray-700"> Betrag (€) * </label>
        <input
          type="number"
          id="amount"
          v-model="journalEntry.amount"
          step="0.01"
          min="0.01"
          required
          placeholder="0,00"
          class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
        />
      </div>

      <div class="space-y-2">
        <label for="description" class="block text-sm font-semibold text-gray-700">
          Beschreibung
        </label>
        <textarea
          id="description"
          v-model="journalEntry.description"
          placeholder="Beschreibung eingeben"
          rows="3"
          class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200"
        ></textarea>
      </div>
    </form>
  </div>

  <!-- Snackbar für Benachrichtigungen -->
  <div
    v-if="showSnackbar"
    :class="snackbarType === 'success' ? 'bg-green-600/90' : 'bg-red-600/90'"
    class="fixed top-4 left-1/2 transform -translate-x-1/2 text-white px-6 py-3 rounded-xl shadow-lg transition-all duration-300 flex items-center"
  >
    <svg
      v-if="snackbarType === 'success'"
      class="h-5 w-5 mr-2"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
    </svg>
    <svg
      v-else
      class="h-5 w-5 mr-2"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
      />
    </svg>
    {{ snackbarMessage }}
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import API_URL from '@/api';

const router = useRouter();

// Snackbar-Funktionalität
const showSnackbar = ref(false);
const snackbarMessage = ref('');
const snackbarType = ref('success');

const showSnackbarMessage = (message, type = 'success') => {
  snackbarMessage.value = message;
  snackbarType.value = type;
  showSnackbar.value = true;
  setTimeout(() => {
    showSnackbar.value = false;
  }, 3000);
};

// Formular-Daten
const journalEntry = ref({
  entry_date: new Date().toISOString().substr(0, 10),
  document_number: '',
  debit_account: '',
  credit_account: '',
  amount: '',
  description: '',
});

const submitJournalEntry = async () => {
  try {
    // CSRF-Token aus Cookies extrahieren
    const csrfToken = document.cookie
      .split(';')
      .find((row) => row.trim().startsWith('csrf_access_token='))
      ?.split('=')[1];

    const response = await fetch(`${API_URL}/api/journal-entries`, {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRF-TOKEN': csrfToken,
      },
      body: JSON.stringify(journalEntry.value),
    });

    if (response.ok) {
      showSnackbarMessage('Buchung erfolgreich erstellt!', 'success');
      // Formular zurücksetzen
      journalEntry.value = {
        entry_date: new Date().toISOString().substr(0, 10),
        document_number: '',
        debit_account: '',
        credit_account: '',
        amount: '',
        description: '',
      };

      // Optional: Zur Übersichtsseite navigieren
      setTimeout(() => {
        router.push({ name: 'journal-entries' });
      }, 1500);
    } else {
      const errorData = await response.json();
      showSnackbarMessage(errorData.message || 'Fehler beim Erstellen der Buchung', 'error');
    }
  } catch (error) {
    console.error('Fehler bei der Buchungserstellung:', error);
    showSnackbarMessage('Ein unerwarteter Fehler ist aufgetreten.', 'error');
  }
};
</script>

<style scoped>
.animate-scale-in {
  animation: scaleIn 0.2s ease-out forwards;
}

.animate-fade-in {
  animation: fadeIn 0.2s ease-out forwards;
}

@keyframes scaleIn {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
