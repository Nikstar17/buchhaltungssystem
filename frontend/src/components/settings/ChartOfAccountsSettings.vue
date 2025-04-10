<template>
  <div class="min-h-screen p-6">
    <h1 class="text-2xl font-bold mb-6 text-gray-800">Kontenrahmen-Einstellungen</h1>

    <div v-if="loading" class="flex justify-center items-center py-10">
      <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
    </div>

    <div v-else class="grid grid-cols-1 gap-6">
      <!-- Kontenrahmen Auswahl Karte -->
      <div class="bg-white rounded-xl shadow-md overflow-hidden p-6">
        <h2 class="text-lg font-semibold mb-4 text-gray-800 border-b pb-2">Kontenrahmen auswählen</h2>

        <div class="mb-6">
          <label for="chart-of-accounts" class="block text-sm font-semibold text-gray-700 mb-2">
            Verfügbare Kontenrahmen
          </label>

          <div class="relative">
            <select id="chart-of-accounts" v-model="selectedChartId" @change="handleChartChange"
              class="w-full px-4 py-2.5 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors duration-200 appearance-none bg-white">
              <option value="" disabled>Bitte wählen Sie einen Kontenrahmen</option>
              <option v-for="chart in chartOfAccounts" :key="chart.id" :value="chart.id">
                {{ chart.name }} {{ isActiveChart(chart.id) ? '(Aktiv)' : '' }}
              </option>
            </select>
            <div class="absolute inset-y-0 right-0 flex items-center px-2 pointer-events-none">
              <svg class="w-5 h-5 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd"
                  d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                  clip-rule="evenodd" />
              </svg>
            </div>
          </div>
        </div>

        <div v-if="selectedChart" class="border-t pt-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h3 class="text-sm uppercase tracking-wide text-gray-500 font-medium mb-1">Name</h3>
              <p class="text-gray-800">{{ selectedChart.name }}</p>
            </div>

            <div>
              <h3 class="text-sm uppercase tracking-wide text-gray-500 font-medium mb-1">Status</h3>
              <p class="text-gray-800">
                <span v-if="isActiveChart(selectedChart.id)" class="text-green-600 font-medium">
                  Aktiv
                </span>
                <span v-else class="text-gray-500">
                  Inaktiv
                </span>
              </p>
            </div>
          </div>

          <div class="mt-4">
            <h3 class="text-sm uppercase tracking-wide text-gray-500 font-medium mb-1">Beschreibung</h3>
            <p class="text-gray-800">{{ selectedChart.description || 'Keine Beschreibung vorhanden' }}</p>
          </div>

          <div class="mt-6 flex justify-end">
            <button @click="activateChart" :disabled="isActiveChart(selectedChart.id) || activating" :class="[
              'px-4 py-2 rounded-lg transition-colors duration-200',
              isActiveChart(selectedChart.id)
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-blue-500 hover:bg-blue-600 text-white'
            ]">
              <span v-if="activating" class="flex items-center">
                <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                  </path>
                </svg>
                Wird aktiviert...
              </span>
              <span v-else-if="isActiveChart(selectedChart.id)">
                Bereits aktiv
              </span>
              <span v-else>
                Aktivieren
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import ChartOfAccountsService from '@/services/chart-of-accounts.service';
import UserService from '@/services/user.service';
import { showSnackbarMessage } from '@/composables/useSnackbar';

const chartOfAccounts = ref([]);
const selectedChartId = ref('');
const loading = ref(false);
const activating = ref(false);
const currentUser = ref(null);

// Berechne das ausgewählte Chart-Objekt basierend auf der ID
const selectedChart = computed(() => {
  if (!selectedChartId.value) return null;
  return chartOfAccounts.value.find(chart => chart.id === selectedChartId.value);
});

// Lade alle verfügbaren Kontenrahmen beim Starten der Komponente
onMounted(async () => {
  await fetchCurrentUser();
  await fetchChartOfAccounts();
});

// Hole den aktuellen Benutzer vom Server
const fetchCurrentUser = async () => {
  try {
    currentUser.value = await UserService.getCurrentUser();
  } catch (error) {
    console.error('Fehler beim Laden des aktuellen Benutzers:', error);
    showSnackbarMessage('Fehler beim Laden des Benutzerprofils', 'error');
  }
};

// Hole alle Kontenrahmen vom Server
const fetchChartOfAccounts = async () => {
  try {
    loading.value = true;
    chartOfAccounts.value = await ChartOfAccountsService.getAll();

    if (chartOfAccounts.value.length > 0) {
      // Wenn der Benutzer bereits einen aktiven Kontenrahmen hat, wähle diesen aus
      if (currentUser.value?.chart_of_accounts_id) {
        selectedChartId.value = currentUser.value.chart_of_accounts_id;
      } else {
        // Ansonsten wähle den ersten Kontenrahmen in der Liste
        selectedChartId.value = chartOfAccounts.value[0].id;
      }
    }
  } catch (error) {
    console.error('Fehler beim Laden der Kontenrahmen:', error);
    showSnackbarMessage('Fehler beim Laden der Kontenrahmen', 'error');
  } finally {
    loading.value = false;
  }
};

// Handler für die Änderung des ausgewählten Kontenrahmens
const handleChartChange = (event) => {
  selectedChartId.value = event.target.value;
};

// Prüft, ob ein Kontenrahmen der aktive Kontenrahmen des Benutzers ist
const isActiveChart = (chartId) => {
  return currentUser.value?.chart_of_accounts_id === chartId;
};

// Aktiviere den ausgewählten Kontenrahmen für den Benutzer
const activateChart = async () => {
  if (!selectedChart.value || isActiveChart(selectedChart.value.id)) return;

  activating.value = true;

  try {
    await UserService.updateUser({
      chart_of_accounts_id: selectedChart.value.id
    });

    // Aktualisiere den Benutzer nach erfolgreicher Aktualisierung
    await fetchCurrentUser();

    showSnackbarMessage(`Kontenrahmen "${selectedChart.value.name}" erfolgreich aktiviert`, 'success');
  } catch (error) {
    console.error('Fehler beim Aktivieren des Kontenrahmens:', error);
    showSnackbarMessage('Fehler beim Aktivieren des Kontenrahmens', 'error');
  } finally {
    activating.value = false;
  }
};
</script>

<style scoped></style>